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


def _topic_words(topic):
    return [word for word in re.findall(r"[A-Za-z0-9]+", topic.lower()) if len(word) > 3]


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
    topic = topic.strip()
    tone = _normalise(tone, "professional")
    audience = _normalise(audience, "your target audience")
    goal = _normalise(goal, "engagement")
    content_type = _normalise(content_type, "educational")
    business = _normalise(business, "your business")
    platform_key = _platform_key(platform)
    platform_rule = PLATFORM_RULES.get(platform_key, PLATFORM_RULES["instagram"])

    hooks = {
        "educational": f"Most {audience} do not need more noise — they need a clearer way to {topic.lower()}.",
        "promotional": f"If you are a {audience} looking to {topic.lower()}, this is worth a closer look.",
        "announcement": f"A new chapter for {business}: {topic}.",
        "story": f"Here is what we learned while working on {topic.lower()}.",
        "problem/solution": f"Still struggling with {topic.lower()}? Start here.",
        "case study": f"What changed when we focused on {topic.lower()}? The results started with one simple shift.",
        "founder": f"A founder lesson we keep coming back to: {topic}.",
    }
    hook = hooks.get(content_type.lower(), hooks["educational"])
    default_cta = platform_rule["cta"]
    requested_cta = cta.strip() if cta else default_cta

    body = (
        f"{hook}\n\n"
        f"For {audience}, the goal is not to do everything at once. Focus on one useful outcome, "
        f"show the practical next step, and make the path from attention to action obvious.\n\n"
        f"At {business}, we believe useful content should help people make a better decision, not just fill a feed. "
        f"If {goal.lower()} is the goal, turn this idea into one concrete action your audience can take today.\n\n"
        f"{requested_cta}"
    )

    tags = [f"#{re.sub(r'[^A-Za-z0-9]', '', business.title())}", "#ContentStrategy"]
    for word in _topic_words(topic)[:2]:
        tag = f"#{word.title()}"
        if tag.lower() not in {item.lower() for item in tags}:
            tags.append(tag)

    return {
        "caption": body,
        "hashtags": tags[:5],
        "hook": hook,
        "cta": requested_cta,
        "platform": platform_rule["name"],
        "format": platform_rule["format"],
        "strategy_note": platform_rule["length"],
    }


def generate_content_ideas(
    business,
    audience="general audience",
    platform="instagram",
    goal="brand awareness",
    industry="",
    offer="",
):
    business = business.strip()
    audience = _normalise(audience, "general audience")
    platform = _normalise(platform, "instagram")
    goal = _normalise(goal, "brand awareness")
    industry = industry.strip()
    offer = offer.strip()

    context = f" in {industry}" if industry else ""
    offer_context = f" using {offer}" if offer else ""
    ideas = [
        {"title": f"The 3 biggest mistakes {audience} make{context}", "format": "Carousel", "pillar": "Education", "goal": "Reach", "hook": "Most people get these three things wrong.", "outline": "Problem → why it happens → practical fix → one action to take today."},
        {"title": f"Behind the scenes: how {business} delivers a result", "format": "Reel", "pillar": "Proof", "goal": "Trust", "hook": "Here is what actually happens behind the scenes.", "outline": "Show the workflow, one decision point, the final output and the lesson."},
        {"title": f"Myth vs fact for {audience}", "format": "Carousel", "pillar": "Authority", "goal": "Saves", "hook": "A popular belief about this problem is only half true.", "outline": "Myth → fact → evidence/example → what to do instead."},
        {"title": f"A 60-second tip to improve one outcome{offer_context}", "format": "Reel", "pillar": "Education", "goal": "Engagement", "hook": "Try this before you spend more time or money.", "outline": "State the problem → demonstrate the tip → show the expected outcome."},
        {"title": f"Answer the question you hear most from {audience}", "format": "Text Post", "pillar": "Education", "goal": "Trust", "hook": "We get asked this all the time.", "outline": "Question → short answer → example → next step."},
        {"title": f"Before vs after: the transformation {business} can create", "format": "Case Study", "pillar": "Proof", "goal": "Leads", "hook": "The biggest change was not what you might expect.", "outline": "Starting point → intervention → measurable/observable change → lesson."},
        {"title": f"Why {business} exists and who it is built for", "format": "Founder Post", "pillar": "Brand", "goal": "Connection", "hook": "We started {business} because this problem kept coming up.", "outline": "Problem → personal insight → mission → who you want to help."},
        {"title": f"A save-worthy checklist for {audience}", "format": "Carousel", "pillar": "Utility", "goal": "Saves", "hook": "Save this checklist before your next project.", "outline": "5–7 checks → common failure point → final action."},
        {"title": f"Break down one feature, service or process in plain language", "format": "Short Video", "pillar": "Education", "goal": "Understanding", "hook": "You do not need the jargon. Here is what it actually does.", "outline": "What it is → why it matters → example → who benefits."},
        {"title": f"A question that reveals what {audience} really wants", "format": "Poll", "pillar": "Research", "goal": "Engagement", "hook": "Which of these would make the biggest difference for you?", "outline": "Ask one focused question → give 3–4 options → use responses for the next content batch."},
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
        {
            "key": "profile",
            "title": "Profile clarity",
            "score": 7,
            "priority": "HIGH",
            "what_good_looks_like": "A visitor understands who you help, what outcome you provide and what to do next within seconds.",
            "action": "Rewrite the bio around audience + outcome + proof + one clear CTA.",
        },
        {
            "key": "content",
            "title": "Content system",
            "score": 6,
            "priority": "HIGH",
            "what_good_looks_like": "Your posts repeat a small set of recognizable pillars instead of relying on random ideas.",
            "action": "Choose 3–5 pillars and assign each a repeatable weekly format.",
        },
        {
            "key": "conversion",
            "title": "Conversion path",
            "score": 5,
            "priority": "CRITICAL",
            "what_good_looks_like": "A high-intent visitor can move from post to enquiry without guessing what happens next.",
            "action": "Use one primary CTA and connect it to a focused landing page, WhatsApp or enquiry form.",
        },
        {
            "key": "proof",
            "title": "Trust signals",
            "score": 6,
            "priority": "HIGH",
            "what_good_looks_like": "Real examples, outcomes, testimonials, process evidence or product progress support your claims.",
            "action": "Publish one proof-led post every week and make the result specific.",
        },
        {
            "key": "discoverability",
            "title": "Discoverability",
            "score": 6,
            "priority": "MEDIUM",
            "what_good_looks_like": "Your profile and content use the language your ideal audience actually searches and recognizes.",
            "action": "Build recurring posts around 5–10 audience problems and use those phrases naturally in profile and content.",
        },
        {
            "key": "consistency",
            "title": "Publishing rhythm",
            "score": 6,
            "priority": "MEDIUM",
            "what_good_looks_like": "You can maintain a predictable cadence without sacrificing usefulness or quality.",
            "action": "Start with 3 useful posts per week and batch-create them from the same content pillars.",
        },
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
        "quick_wins": [
            "Clarify the profile promise and use one primary CTA.",
            "Create three recurring content pillars tied to audience problems.",
            "Publish one proof/case-study post every week.",
            "Make every high-intent post point to the same conversion path.",
        ],
        "seven_day_plan": [
            "Day 1 — Rewrite your profile promise and CTA.",
            "Day 2 — Define three audience-led content pillars.",
            "Day 3 — Create one educational post from a real customer problem.",
            "Day 4 — Publish a proof, case study or behind-the-scenes post.",
            "Day 5 — Create a save-worthy checklist or framework.",
            "Day 6 — Review which CTA appears most often and simplify it.",
            "Day 7 — Batch next week's three posts using the same pillars.",
        ],
        "next_step": "Fix the conversion path first, then build a repeatable content system around the audience problems you solve.",
    }
