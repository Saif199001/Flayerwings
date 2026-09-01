from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlparse

from .meta_client import MetaGraphError, get_business_discovery, meta_graph_configured


def _username_from_url(profile_url):
    parsed = urlparse(profile_url)
    if parsed.netloc.lower().replace("www.", "") not in {"instagram.com", "facebook.com", "x.com", "twitter.com", "linkedin.com"}:
        raise MetaGraphError("Enter a supported social profile URL. Instagram is currently supported for live Meta analysis.")
    path = parsed.path.strip("/").split("/")
    username = path[0] if path else ""
    if not username or username.lower() in {"p", "reel", "reels", "explore", "accounts"}:
        raise MetaGraphError("The profile URL must point directly to an Instagram username.")
    return username


def _days_since(timestamp):
    if not timestamp:
        return None
    try:
        value = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return max(0, (datetime.now(timezone.utc) - value).days)
    except ValueError:
        return None


def _normalised_media(profile):
    return [item for item in (profile.get("media", {}).get("data", []) or []) if item.get("id")]


def _score_profile(profile):
    score = 0
    reasons = []
    bio = (profile.get("biography") or "").strip()
    website = (profile.get("website") or "").strip()
    name = (profile.get("name") or "").strip()
    if name:
        score += 2
    else:
        reasons.append("Add a clear display name that states the category or outcome you provide.")
    if bio:
        score += 2
        if len(bio) >= 80:
            score += 1
        else:
            reasons.append("Expand the bio so the audience, outcome and differentiator are immediately clear.")
    else:
        reasons.append("Add a concise value proposition to the bio.")
    if website:
        score += 2
    else:
        reasons.append("Add a website or primary conversion destination so interested visitors have somewhere useful to go.")
    return min(10, score), reasons


def _score_content(media):
    if not media:
        return 0, ["Publish enough recent content for the audit to identify a repeatable content pattern."]
    formats = Counter((item.get("media_product_type") or item.get("media_type") or "unknown").lower() for item in media)
    recent = [item for item in media if (_days_since(item.get("timestamp")) or 999) <= 14]
    score = min(4, len(recent)) + min(3, len(formats))
    score = min(10, score)
    actions = []
    if len(recent) < 3:
        actions.append("Increase recent publishing consistency; aim for at least three useful posts per two weeks.")
    if len(formats) == 1:
        actions.append("Test a second format so the content system can serve both discovery and deeper education.")
    return score, actions


def _score_conversion(profile):
    bio = (profile.get("biography") or "").lower()
    website = (profile.get("website") or "").strip()
    cta_terms = ("dm", "book", "call", "visit", "learn", "apply", "shop", "get", "start", "contact")
    has_cta = any(term in bio for term in cta_terms)
    score = 4 + (3 if has_cta else 0) + (3 if website else 0)
    action = "Keep one primary CTA and make the next step obvious from the profile."
    if not has_cta:
        action = "Add one explicit CTA to the bio and make it match the primary conversion goal."
    return min(10, score), action


def _score_proof(media):
    proof_terms = ("result", "case study", "client", "customer", "before", "after", "testimonial", "review", "worked", "outcome")
    proof_count = sum(1 for item in media if any(term in (item.get("caption") or "").lower() for term in proof_terms))
    score = min(10, 4 + proof_count * 2)
    action = "Publish more specific proof: before/after, customer outcome, case study or process evidence." if proof_count < 2 else "Keep turning real outcomes into recurring proof-led content."
    return score, action


def _engagement_summary(profile, media):
    followers = profile.get("followers_count") or 0
    rows = []
    for item in media:
        likes = item.get("like_count") or 0
        comments = item.get("comments_count") or 0
        interactions = likes + comments
        rate = round((interactions / followers) * 100, 2) if followers else None
        rows.append({
            "id": item.get("id"),
            "timestamp": item.get("timestamp"),
            "media_type": item.get("media_product_type") or item.get("media_type"),
            "permalink": item.get("permalink"),
            "likes": likes,
            "comments": comments,
            "interactions": interactions,
            "engagement_rate_percent": rate,
        })
    ranked = sorted(rows, key=lambda item: item["interactions"], reverse=True)
    return {
        "followers": followers,
        "sample_size": len(rows),
        "average_interactions": round(sum(row["interactions"] for row in rows) / len(rows), 1) if rows else 0,
        "average_engagement_rate_percent": round(sum(row["engagement_rate_percent"] or 0 for row in rows) / len(rows), 2) if rows and followers else None,
        "top_posts": ranked[:3],
        "posts": rows,
    }


def _build_meta_audit(business, profile_url):
    username = _username_from_url(profile_url)
    profile = get_business_discovery(username)
    if not profile:
        raise MetaGraphError("Meta could not find a Business or Creator profile for that username. The target may be a personal account or unavailable to Business Discovery.")

    media = _normalised_media(profile)
    profile_score, profile_actions = _score_profile(profile)
    content_score, content_actions = _score_content(media)
    conversion_score, conversion_action = _score_conversion(profile)
    proof_score, proof_action = _score_proof(media)
    engagement = _engagement_summary(profile, media)
    scores = [profile_score, content_score, conversion_score, proof_score]
    overall = round(sum(scores) / len(scores), 1)

    recent_days = [_days_since(item.get("timestamp")) for item in media]
    recent_days = [value for value in recent_days if value is not None]
    cadence = {
        "sample_posts": len(media),
        "posts_in_last_14_days": sum(1 for value in recent_days if value <= 14),
        "latest_post_days_ago": min(recent_days) if recent_days else None,
    }

    return {
        "business": business,
        "profile_url": profile_url,
        "platform": "Instagram",
        "audit_type": "meta_live_profile_audit",
        "data_source": "Meta Graph API Business Discovery",
        "profile": {
            "username": profile.get("username"),
            "name": profile.get("name"),
            "biography": profile.get("biography"),
            "website": profile.get("website"),
            "followers_count": profile.get("followers_count"),
            "follows_count": profile.get("follows_count"),
            "media_count": profile.get("media_count"),
        },
        "score": overall,
        "score_scale": 10,
        "checks": [
            {"key": "profile", "title": "Profile clarity", "score": profile_score, "priority": "HIGH", "evidence": profile_actions or ["Display name, bio and website are present."], "action": profile_actions[0] if profile_actions else "Keep the profile promise specific and outcome-led."},
            {"key": "content", "title": "Content system", "score": content_score, "priority": "HIGH", "evidence": [f"{len(media)} recent media items were sampled.", f"{len(recent_days) and sum(1 for value in recent_days if value <= 14) or 0} were published in the last 14 days."], "action": content_actions[0] if content_actions else "Keep the strongest format mix and repeat the topics that produce the best response."},
            {"key": "conversion", "title": "Conversion path", "score": conversion_score, "priority": "CRITICAL", "evidence": ["Website is present." if profile.get("website") else "No website was returned by Meta.", "Bio contains a CTA." if conversion_score >= 7 else "No clear CTA language was detected in the bio."], "action": conversion_action},
            {"key": "proof", "title": "Trust signals", "score": proof_score, "priority": "HIGH", "evidence": [f"{sum(1 for item in media if any(term in (item.get('caption') or '').lower() for term in ('result','case study','client','customer','before','after','testimonial','review','worked','outcome')))} sampled posts contain proof-oriented language."], "action": proof_action},
        ],
        "performance": engagement,
        "publishing": cadence,
        "quick_wins": profile_actions[:2] + [conversion_action, proof_action],
        "seven_day_plan": [
            "Day 1 — Rewrite the profile promise around audience + outcome + proof + one CTA.",
            "Day 2 — Identify the three sampled posts with the strongest interaction and extract their topic/format pattern.",
            "Day 3 — Create one educational post addressing a repeated audience problem.",
            "Day 4 — Publish one proof-led post using a real outcome or process example.",
            "Day 5 — Create one save-worthy checklist based on the strongest topic pattern.",
            "Day 6 — Tighten every high-intent caption around the same conversion action.",
            "Day 7 — Batch next week's posts using the formats and themes that performed best in the sample.",
        ],
        "next_step": "Use the live profile evidence first: fix the conversion path, then repeat the content patterns that are already earning the strongest response.",
        "confidence_note": "This audit uses live data returned by Meta for an Instagram Business or Creator profile. It does not scrape private data and does not invent reach or engagement metrics. Engagement rates are calculated only from the sampled media interactions and the returned follower count.",
    }


def run_live_social_audit(business, profile_url):
    if not meta_graph_configured():
        return None
    return _build_meta_audit(business, profile_url)
