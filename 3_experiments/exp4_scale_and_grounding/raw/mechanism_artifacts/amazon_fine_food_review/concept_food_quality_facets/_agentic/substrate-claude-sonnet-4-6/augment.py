import csv
import re

# Food quality facets with associated keywords/phrases
FACETS = {
    "facet_taste": [
        r"\btaste\b", r"\bflavor\b", r"\bflavour\b", r"\bdelicious\b", r"\byummy\b",
        r"\bsweet\b", r"\bsalty\b", r"\bbitter\b", r"\bsour\b", r"\bumami\b",
        r"\bsavory\b", r"\bsavoury\b", r"\btangy\b", r"\bspicy\b", r"\brich\b",
        r"\bbland\b", r"\btasty\b", r"\bpalatable\b", r"\bmouth\b", r"\baftertaste\b",
        r"\bflavored\b", r"\bflavoured\b", r"\bflavorful\b", r"\bflavorless\b",
        r"\btasteless\b", r"\bgood taste\b", r"\bbad taste\b",
    ],
    "facet_texture": [
        r"\btexture\b", r"\bcrunchy\b", r"\bcrispy\b", r"\bsoft\b", r"\bchewy\b",
        r"\bhard\b", r"\btender\b", r"\bsmooth\b", r"\bgritty\b", r"\bmushy\b",
        r"\bthick\b", r"\bthin\b", r"\bflaky\b", r"\bcreamy\b", r"\bgooey\b",
        r"\bfirm\b", r"\bsticky\b", r"\bcrunchy\b", r"\bmoist\b", r"\bdry\b",
        r"\bcrumbly\b", r"\bsilky\b", r"\bgrainy\b", r"\bchewiness\b", r"\bcrispness\b",
    ],
    "facet_freshness": [
        r"\bfresh\b", r"\bfreshness\b", r"\bstale\b", r"\bexpired\b", r"\bexpiration\b",
        r"\bspoiled\b", r"\brancid\b", r"\bmoldy\b", r"\bold\b", r"\bshelf.?life\b",
        r"\bbest.?by\b", r"\buse.?by\b", r"\bexpiry\b", r"\brotted\b", r"\bfresh.?tasting\b",
        r"\bnot fresh\b", r"\bday.?old\b",
    ],
    "facet_smell_aroma": [
        r"\bsmell\b", r"\baroma\b", r"\bscent\b", r"\bodor\b", r"\bodour\b",
        r"\bfragrant\b", r"\bfragrance\b", r"\bstinky\b", r"\bstench\b",
        r"\bfoul smell\b", r"\bnice smell\b", r"\bgood smell\b", r"\bbad smell\b",
        r"\bsmells like\b", r"\bsmells good\b", r"\bsmells bad\b",
    ],
    "facet_appearance": [
        r"\bappearance\b", r"\bcolor\b", r"\bcolour\b", r"\blook\b", r"\blooks\b",
        r"\bpresentation\b", r"\bbeautiful\b", r"\bugly\b", r"\bvibrant\b",
        r"\bbrown\b", r"\bgreen\b", r"\bright\b", r"\bdark\b", r"\blight.?colored\b",
        r"\bvisual\b", r"\bappetizing\b", r"\bappetising\b", r"\bunappetizing\b",
    ],
    "facet_ingredients_nutrition": [
        r"\bingredient\b", r"\bnatural\b", r"\borganic\b", r"\bartificial\b",
        r"\bpreservative\b", r"\badditive\b", r"\bnutrition\b", r"\bnutritious\b",
        r"\bhealthy\b", r"\bunhealthy\b", r"\bcalorie\b", r"\bprotein\b",
        r"\bsugar\b", r"\bsodium\b", r"\bfat\b", r"\bfiber\b", r"\bvitamin\b",
        r"\bgmo\b", r"\bnon.?gmo\b", r"\bgluten\b", r"\bdairy.?free\b",
        r"\bvegan\b", r"\bvegetarian\b", r"\ball.?natural\b",
    ],
    "facet_packaging_quantity": [
        r"\bpackag\b", r"\bpacket\b", r"\bcontainer\b", r"\bjar\b", r"\bbag\b",
        r"\bbox\b", r"\bcan\b", r"\bbottle\b", r"\bsize\b", r"\bamount\b",
        r"\bquantity\b", r"\bportion\b", r"\bserving\b", r"\bvalue\b",
        r"\bprice\b", r"\boverpriced\b", r"\baffordable\b", r"\bworth\b",
        r"\bcost\b", r"\bexpensive\b", r"\bcheap\b", r"\boverpriced\b",
    ],
    "facet_consistency_brand": [
        r"\bconsisten\b", r"\bquality control\b", r"\bbatch\b", r"\bformula\b",
        r"\brecipe changed\b", r"\bused to\b", r"\bbrand\b", r"\breliable\b",
        r"\bunreliable\b", r"\bsame as before\b", r"\bdifferent from\b",
        r"\bchanged\b", r"\bdisappoint\b", r"\bexpect\b", r"\bstandard\b",
    ],
}

def classify_review(text, summary):
    combined = (str(text) + " " + str(summary)).lower()
    result = {}
    for facet, patterns in FACETS.items():
        matched = any(re.search(p, combined) for p in patterns)
        result[facet] = "1" if matched else "0"
    # Derive a primary_quality_facet: whichever facet first appears (by keyword position)
    first_match_pos = {}
    for facet, patterns in FACETS.items():
        positions = []
        for p in patterns:
            m = re.search(p, combined)
            if m:
                positions.append(m.start())
        if positions:
            first_match_pos[facet] = min(positions)
    if first_match_pos:
        primary = min(first_match_pos, key=first_match_pos.get)
        # Strip "facet_" prefix and make readable
        result["primary_quality_facet"] = primary.replace("facet_", "")
    else:
        result["primary_quality_facet"] = "none"
    return result

input_path = "input.csv"
output_path = "augment.csv"

new_cols = list(FACETS.keys()) + ["primary_quality_facet"]

with open(input_path, newline="", encoding="utf-8") as fin, \
     open(output_path, "w", newline="", encoding="utf-8") as fout:
    reader = csv.DictReader(fin)
    fieldnames = reader.fieldnames + new_cols
    writer = csv.DictWriter(fout, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        annotations = classify_review(row.get("Text", ""), row.get("Summary", ""))
        row.update(annotations)
        writer.writerow(row)

print("Done.")
