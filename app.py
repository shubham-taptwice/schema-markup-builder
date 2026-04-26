import gradio as gr
import json


def build_faq_schema(faqs_raw):
    pairs = []
    lines = [l.strip() for l in faqs_raw.strip().splitlines() if l.strip()]
    i = 0
    while i < len(lines):
        if lines[i].startswith("Q:"):
            q = lines[i][2:].strip()
            a = ""
            if i + 1 < len(lines) and lines[i + 1].startswith("A:"):
                a = lines[i + 1][2:].strip()
                i += 1
            pairs.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
        i += 1

    if not pairs:
        return "No Q&A pairs found. Use the format:\nQ: Your question\nA: Your answer"

    schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": pairs}
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def build_org_schema(name, url, description, logo_url, phone, email, linkedin, twitter):
    schema = {"@context": "https://schema.org", "@type": "Organization", "name": name, "url": url}
    if description: schema["description"] = description
    if logo_url: schema["logo"] = logo_url
    if phone: schema["telephone"] = phone
    if email: schema["email"] = email
    same_as = [s.strip() for s in [linkedin, twitter] if s.strip()]
    if same_as: schema["sameAs"] = same_as
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def build_localbiz_schema(name, url, description, phone, email, street, city, state, postal, country, opens, closes, price_range):
    schema = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": name, "url": url}
    if description: schema["description"] = description
    if phone: schema["telephone"] = phone
    if email: schema["email"] = email
    if street or city:
        schema["address"] = {
            "@type": "PostalAddress",
            "streetAddress": street,
            "addressLocality": city,
            "addressRegion": state,
            "postalCode": postal,
            "addressCountry": country or "US",
        }
    if opens and closes:
        schema["openingHours"] = f"Mo-Fr {opens}-{closes}"
    if price_range:
        schema["priceRange"] = price_range
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


def build_article_schema(headline, author_name, author_url, pub_date, mod_date, image_url, publisher_name, publisher_logo, description, article_url):
    schema = {"@context": "https://schema.org", "@type": "Article", "headline": headline}
    if description: schema["description"] = description
    if article_url: schema["url"] = article_url
    if image_url: schema["image"] = image_url
    if pub_date: schema["datePublished"] = pub_date
    if mod_date: schema["dateModified"] = mod_date
    if author_name:
        author = {"@type": "Person", "name": author_name}
        if author_url: author["url"] = author_url
        schema["author"] = author
    if publisher_name:
        pub = {"@type": "Organization", "name": publisher_name}
        if publisher_logo: pub["logo"] = {"@type": "ImageObject", "url": publisher_logo}
        schema["publisher"] = pub
    return f'<script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n</script>'


with gr.Blocks(theme=gr.themes.Soft(), title="Schema Markup Builder by Taptwice Media") as demo:
    gr.Markdown("# Schema Markup Builder by Taptwice Media")
    gr.HTML(
        'Generate JSON-LD structured data for your website. Copy the output and paste it into your page\'s <code>&lt;head&gt;</code>. '
        'Built by <a href="https://taptwicemedia.com" target="_blank">Taptwice Media</a> — the AEO &amp; GEO specialists.'
    )

    with gr.Tabs():
        with gr.Tab("FAQPage"):
            gr.Markdown("**Best for AEO** — tells AI engines your exact Q&A content. Paste Q&A pairs below.")
            faq_input = gr.Textbox(
                label="Q&A Pairs",
                placeholder="Q: What is AEO?\nA: AEO stands for Answer Engine Optimization.\n\nQ: How does AEO work?\nA: It optimizes your content to appear in AI-generated answers.",
                lines=12,
            )
            faq_btn = gr.Button("Generate FAQPage Schema", variant="primary")
            faq_out = gr.Textbox(label="Copy this into your <head>", lines=20)
            faq_btn.click(build_faq_schema, inputs=[faq_input], outputs=[faq_out])

        with gr.Tab("Organization"):
            with gr.Row():
                org_name = gr.Textbox(label="Organization Name *")
                org_url = gr.Textbox(label="Website URL *")
            org_desc = gr.Textbox(label="Description", lines=2)
            with gr.Row():
                org_logo = gr.Textbox(label="Logo URL")
                org_phone = gr.Textbox(label="Phone")
                org_email = gr.Textbox(label="Email")
            with gr.Row():
                org_linkedin = gr.Textbox(label="LinkedIn URL")
                org_twitter = gr.Textbox(label="Twitter/X URL")
            org_btn = gr.Button("Generate Organization Schema", variant="primary")
            org_out = gr.Textbox(label="Copy this into your <head>", lines=20)
            org_btn.click(build_org_schema, inputs=[org_name, org_url, org_desc, org_logo, org_phone, org_email, org_linkedin, org_twitter], outputs=[org_out])

        with gr.Tab("LocalBusiness"):
            with gr.Row():
                lb_name = gr.Textbox(label="Business Name *")
                lb_url = gr.Textbox(label="Website URL *")
            lb_desc = gr.Textbox(label="Description", lines=2)
            with gr.Row():
                lb_phone = gr.Textbox(label="Phone")
                lb_email = gr.Textbox(label="Email")
                lb_price = gr.Textbox(label="Price Range (e.g. $$)")
            with gr.Row():
                lb_street = gr.Textbox(label="Street Address")
                lb_city = gr.Textbox(label="City")
                lb_state = gr.Textbox(label="State/Region")
            with gr.Row():
                lb_postal = gr.Textbox(label="Postal Code")
                lb_country = gr.Textbox(label="Country Code", value="US")
            with gr.Row():
                lb_opens = gr.Textbox(label="Opens (e.g. 09:00)")
                lb_closes = gr.Textbox(label="Closes (e.g. 18:00)")
            lb_btn = gr.Button("Generate LocalBusiness Schema", variant="primary")
            lb_out = gr.Textbox(label="Copy this into your <head>", lines=20)
            lb_btn.click(build_localbiz_schema, inputs=[lb_name, lb_url, lb_desc, lb_phone, lb_email, lb_street, lb_city, lb_state, lb_postal, lb_country, lb_opens, lb_closes, lb_price], outputs=[lb_out])

        with gr.Tab("Article"):
            art_headline = gr.Textbox(label="Headline *")
            art_desc = gr.Textbox(label="Description", lines=2)
            art_url = gr.Textbox(label="Article URL")
            with gr.Row():
                art_author = gr.Textbox(label="Author Name")
                art_author_url = gr.Textbox(label="Author URL")
            with gr.Row():
                art_pub_date = gr.Textbox(label="Published Date (YYYY-MM-DD)")
                art_mod_date = gr.Textbox(label="Modified Date (YYYY-MM-DD)")
            art_image = gr.Textbox(label="Image URL")
            with gr.Row():
                art_publisher = gr.Textbox(label="Publisher Name")
                art_publisher_logo = gr.Textbox(label="Publisher Logo URL")
            art_btn = gr.Button("Generate Article Schema", variant="primary")
            art_out = gr.Textbox(label="Copy this into your <head>", lines=20)
            art_btn.click(build_article_schema, inputs=[art_headline, art_author, art_author_url, art_pub_date, art_mod_date, art_image, art_publisher, art_publisher_logo, art_desc, art_url], outputs=[art_out])

if __name__ == "__main__":
    demo.launch()
