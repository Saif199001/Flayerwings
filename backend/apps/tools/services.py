import re
from urllib.parse import urlparse


PLATFORM_RULES = {
    "instagram": {
        "name": "Instagram",
        "length": "Keep the opening tight and make the first two lines earn the scroll.",
        "format": "Reel, carousel or single-image post",
        "cta": "Save this for later and DM us if you want help applying it.",
    },
    "linkedin": {
        "name": "LinkedIn",
        "length": "Lead with a clear business insight, then support it with a practical example.",
        "format": "Text post or document carousel",
        "cta": "What would you add? Share your experience in the comments.",
    },
    "facebook": {
        "name": "Facebook",
        "length": "Make the value obvious early and invite a simple conversation.",
        "format": "Image, short video or text post",
        "cta": "Comment with your biggest challenge and we will help you think it through.",
    },
    "x": {
        "name": "X",
        "length": "Use a sharp point of view and remove anything that does not move the idea forward.",
        "format": "Short post or thread",
        "cta": "Reply with your take.",
    },
}


def _normalise(value, fallback):
    value = (value or "").strip()
    return value or fallback


def _platform_key(platform):
    value = _normalise(platform, "instagram").lower().replace("twitter", "x").replace("(x)", "x")
    return value


def _clean_phrase(value, fallback):
    value = re.sub(r"\s+", " ", (value or "").strip(" .,!?:;-"))
    return value or fallback


def _audience_phrase(audience):
    phrase = _clean_phrase(audience, "your audience")
    lowered = phrase.lower()
    if lowered.startswith(("a ", "an ", "the ")):
        return phrase
    if re.search(r"\b(startups|founders|freelancers|business owners|brands|marketers|creators|teams|businesses)\b", lowered):
        return phrase
    return phrase


def _topic_words(topic):
    return [word for word in re.findall(r"[A-Za-z0-9]+", topic.lower()) if len(word) > 3]


def _safe_hashtag(value):
    words = re.findall(r"[A-Za-z0-9]+", value)
    return "#" + "".join(word.title() for word in words[:4]) if words else ""


def _tone_guidance(tone):
    tone_key = tone.lower()
    return {
        "professional": "Be clear, credible and practical. Avoid hype.",
        "friendly": "Sound warm, conversational and helpful. Keep the language natural.",
        "bold": "Take a confident point of view and make the main idea unmistakable.",
        "casual": "Write like a smart conversation: simple, direct and relaxed.",
        "educational": "Teach one useful idea clearly and finish with an actionable takeaway.",
        "persuasive": "Focus on the problem, the useful outcome and a credible reason to act.",
    }.get(tone_key, "Keep the language clear, natural and useful.")


def generate_caption(
    topic,
    tone="professional",
    platform="instagram",
    audience="your target audience",
    goal="engagement",
    content_type="educational",
    cta="",
    business="your business",
):
    topic = _clean_phrase(topic, "your topic")
    tone = _normalise(tone, "professional")
    audience = _audience_phrase(audience)
    goal = _clean_phrase(goal, "engagement")
    content_type = _normalise(content_type, "educational")
    business = _clean_phrase(business, "your business")
    platform_key = _platform_key(platform)
    platform_rule = PLATFORM_RULES.get(platform_key, PLATFORM_RULES["instagram"])
    topic_lower = topic.lower()
    content_key = content_type.lower()

    hooks = {
        "educational": f"{audience.title()} do not need more information about {topic} — they need a clearer way to use it.",
        "promotional": f"If {audience.lower()} want a better way to {topic_lower}, start with the outcome that matters most.",
        "announcement": f"A new step for {business}: {topic}.",
        "story": f"One lesson we learned while working on {topic}: the simple approach usually wins.",
        "problem/solution": f"If {topic_lower} keeps getting in the way, start by fixing the first bottleneck.",
        "case study": f"What changes when {audience.lower()} approach {topic} with a clear system? Start with one measurable outcome.",
        "founder": f"Building {business} has reinforced one lesson for us: {topic}.",
    }
    hook = hooks.get(content_key, hooks["educational"])
    requested_cta = _clean_phrase(cta, platform_rule["cta"])
    tone_line = _tone_guidance(tone)

    body = (
        f"{hook}\n\n"
        f"The useful approach is to focus on one outcome instead of trying to solve everything at once. "
        f"For {audience.lower()}, that means turning {topic} into a practical next step that can be understood and used today.\n\n"
        f"At {business}, we use this principle to keep content useful: explain the problem, show what changes, "
        f"and give people a clear action to take. The goal here is {goal.lower()}, not simply more attention.\n\n"
        f"{requested_cta}"
    )

    tags = []
    business_tag = _safe_hashtag(business)
    if business_tag:
        tags.append(business_tag)
    for value in [topic, goal, platform_rule["name"]]:
        tag = _safe_hashtag(value)
        if tag and tag.lower() not in {item.lower() for item in tags}:
            tags.append(tag)
    tags.append("#ContentStrategy")

    return {
        "caption": body,
        "hashtags": tags[:5],
        "hook": hook,
        "cta": requested_cta,
        "platform": platform_rule["name"],
        "format": platform_rule["format"],
        "strategy_note": f"{platform_rule['length']} {tone_line}",
    }


def _goal_language(goal):
    key = goal.lower()
    if "lead" in key:
        return "lead generation"
    if "sales" in key or "conversion" in key:
        return "conversion"
    if "engagement" in key:
        return "engagement"
    if "reach" in key or "awareness" in key:
        return "reach and awareness"
    return goal.lower()


def generate_content_ideas(
    business,
    audience="general audience",
    platform="instagram",
    goal="brand awareness",
    industry="",
    offer="",
):
    business = _clean_phrase(business, "your business")
    audience = _audience_phrase(audience)
    platform = _normalise(platform, "instagram")
    goal = _clean_phrase(goal, "brand awareness")
    industry = _clean_phrase(industry, "")
    offer = _clean_phrase(offer, "")
    goal_label = _goal_language(goal)
    context = industry or "your market"
    offer_label = offer or f"your {context} offer"
    audience_lower = audience.lower()
    business_lower = business.lower()

    ideas = [
        {"title": f"The 3 biggest {context} mistakes {audience_lower} should avoid", "format": "Carousel", "pillar": "Education", "goal": "Reach", "hook": "Most teams lose time here without realizing it.", "outline": f"Problem → why it happens → practical fix → one action for {audience_lower} to take today."},
        {"title": f"Behind the scenes: how {business} turns {offer_label.lower()} into a real outcome", "format": "Reel", "pillar": "Proof", "goal": "Trust", "hook": "Here is what actually happens between the brief and the final result.", "outline": "Show the starting problem → key decisions → workflow → final output → lesson."},
        {"title": f"Myth vs fact: what {audience_lower} should know about {context}", "format": "Carousel", "pillar": "Authority", "goal": "Saves", "hook": "A common belief about this problem is only half true.", "outline": "Myth → fact → evidence or example → what to do instead."},
        {"title": f"A 60-second way to improve {goal_label} with {offer_label.lower()}", "format": "Reel", "pillar": "Education", "goal": "Engagement", "hook": "Try this before you spend more time or money.", "outline": "State the problem → demonstrate one change → show the expected outcome → invite a response."},
        {"title": f"Answer the question {audience_lower} ask before choosing {offer_label.lower()}", "format": "Text Post", "pillar": "Education", "goal": "Trust", "hook": "If you are asking this, you are probably not the only one.", "outline": "Question → clear answer → example → decision rule → next step."},
        {"title": f"Before vs after: what changes when {audience_lower} use a better {context} process", "format": "Case Study", "pillar": "Proof", "goal": "Leads", "hook": "The biggest improvement is often the part nobody notices at first.", "outline": "Starting point → intervention → observable change → business impact → lesson."},
        {"title": f"Why {business} built its approach to {offer_label.lower()}", "format": "Founder Post", "pillar": "Brand", "goal": "Connection", "hook": f"We kept seeing the same problem, so we built a better way to approach it.", "outline": "Customer problem → what was missing → your approach → principle → who it is for."},
        {"title": f"A save-worthy checklist for {audience_lower} evaluating {offer_label.lower()}", "format": "Carousel", "pillar": "Utility", "goal": "Saves", "hook": "Save this before you make your next decision.", "outline": "5–7 checks → common warning signs → good benchmark → final action."},
        {"title": f"Explain {offer_label.lower()} without the jargon", "format": "Short Video", "pillar": "Education", "goal": "Understanding", "hook": "You do not need the jargon. Here is what actually matters.", "outline": "What it is → why it matters → simple example → who benefits → first step."},
        {"title": f"One question to learn what {audience_lower} really want from {context}", "format": "Poll", "pillar": "Research", "goal": "Engagement", "hook": "Which of these would make the biggest difference for you right now?", "outline": "Ask one focused question → offer 3–4 meaningful options → use responses to plan the next content batch."},
    ]
    return {
        "business": business,
        "audience": audience,
        "platform": platform,
        "goal": goal,
        "content_pillars": ["Education", "Authority", "Proof", "Brand", "Utility"],
        "ideas": ideas,
    }


def _platform_from_url(profile_url):
    host = urlparse(profile_url).netloc.lower()
    if "linkedin" in host:
        return "LinkedIn"
    if "facebook" in host:
        return "Facebook"
    if "twitter" in host or host == "x.com":
        return "X"
    return "Instagram" if "instagram" in host else "Social profile"


def run_social_audit(business, profile_url):
    business = business.strip()
    profile_url = profile_url.strip()
    platform = _platform_from_url(profile_url)

    checks = [
        {"key": "profile", "title": "Profile clarity", "score": 7, "priority": "HIGH", "what_good_looks_like": "A visitor understands who you help, what outcome you provide and what to do next within seconds.", "action": "Rewrite the bio around audience + outcome + proof + one clear CTA."},
        {"key": "content", "title": "Content system", "score": 6, "priority": "HIGH", "what_good_looks_like": "Your posts repeat a small set of recognizable pillars instead of relying on random ideas.", "action": "Choose 3–5 pillars and assign each a repeatable weekly format."},
        {"key": "conversion", "title": "Conversion path", "score": 5, "priority": "CRITICAL", "what_good_looks_like": "A high-intent visitor can move from post to enquiry without guessing what happens next.", "action": "Use one primary CTA and connect it to a focused landing page, WhatsApp or enquiry form."},
        {"key": "proof", "title": "Trust signals", "score": 6, "priority": "HIGH", "what_good_looks_like": "Real examples, outcomes, testimonials, process evidence or product progress support your claims.", "action": "Publish one proof-led post every week and make the result specific."},
        {"key": "discoverability", "title": "Discoverability", "score": 6, "priority": "MEDIUM", "what_good_looks_like": "Your profile and content use the language your ideal audience actually searches and recognizes.", "action": "Build recurring posts around 5–10 audience problems and use those phrases naturally in profile and content."},
        {"key": "consistency", "title": "Publishing rhythm", "score": 6, "priority": "MEDIUM", "what_good_looks_like": "You can maintain a predictable cadence without sacrificing usefulness or quality.", "action": "Start with 3 useful posts per week and batch-create them from the same content pillars."},
    ]

    average = round(sum(item["score"] for item in checks) / len(checks), 1)
    return {
        "business": business,
        "profile_url": profile_url,
        "platform": platform,
        "score": average,
        "score_scale": 10,
        "audit_type": "strategy_baseline",
        "confidence_note": "This is a strategic baseline based on the information provided and the profile URL. It does not scrape private account data or invent follower, reach or engagement metrics.",
        "checks": checks,
        "quick_wins": ["Clarify the profile promise and use one primary CTA.", "Create three recurring content pillars tied to audience problems.", "Publish one proof/case-study post every week.", "Make every high-intent post point to the same conversion path."],
        "seven_day_plan": ["Day 1 — Rewrite your profile promise and CTA.", "Day 2 — Define three audience-led content pillars.", "Day 3 — Create one educational post from a real customer problem.", "Day 4 — Publish a proof, case study or behind-the-scenes post.", "Day 5 — Create a save-worthy checklist or framework.", "Day 6 — Review which CTA appears most often and simplify it.", "Day 7 — Batch next week's three posts using the same pillars."],
        "next_step": "Fix the conversion path first, then build a repeatable content system around the audience problems you solve.",
    }
