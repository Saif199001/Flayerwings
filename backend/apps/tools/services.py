def generate_caption(topic, tone="professional", platform="instagram"):
    tone_text = tone.strip() or "professional"
    platform_text = platform.strip().lower() or "instagram"
    return {
        "caption": f"{topic.strip()} — {tone_text} content made for {platform_text}. Share the value, invite the conversation, and give your audience one clear next step.",
        "hashtags": ["#FlayerWings", "#SocialMedia", "#DigitalGrowth"],
    }


def generate_content_ideas(business, audience="general audience", platform="instagram"):
    business = business.strip()
    audience = audience.strip() or "general audience"
    platform = platform.strip() or "instagram"
    ideas = [
        f"3 common problems {audience} face with {business}",
        f"A behind-the-scenes look at how {business} delivers its work",
        f"Myth vs fact: what {audience} should know about {business}",
        f"A quick tip that helps {audience} get better results from {business}",
        f"Customer question of the week about {business}",
        f"Before vs after: the transformation {business} can create",
        f"A short founder story: why {business} exists",
        f"A checklist {audience} can save and use today",
        f"A product/service feature explained in simple language",
        f"A poll or question designed for {audience} on {platform}",
    ]
    return {"ideas": ideas}


def run_social_audit(business, profile_url):
    checks = [
        {"key": "profile", "title": "Profile clarity", "score": 7, "tip": "Make the bio immediately explain who you help, what you offer and the next action."},
        {"key": "content", "title": "Content consistency", "score": 6, "tip": "Use repeatable content pillars and a realistic weekly publishing rhythm."},
        {"key": "conversion", "title": "Conversion path", "score": 5, "tip": "Give visitors one obvious next step such as a free audit, WhatsApp or enquiry form."},
        {"key": "proof", "title": "Trust signals", "score": 6, "tip": "Show genuine work, testimonials, process or product progress instead of generic claims."},
    ]
    average = round(sum(item["score"] for item in checks) / len(checks), 1)
    return {"business": business.strip(), "profile_url": profile_url.strip(), "score": average, "checks": checks, "next_step": "Start with the lowest-scoring area and improve one conversion path before increasing posting volume."}
