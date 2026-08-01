Exit code: 0
Wall time: 0.2 seconds
Output:
# TikTok Script Pattern Library

Use this compact index before writing scripts, shot tables, image prompts, or video prompts. The full source extraction from the user's DOCX is available at [tiktok-script-library-full-extract.md](tiktok-script-library-full-extract.md), the Feishu code-block collection is available at [feishu-commerce-code-block-library.md](feishu-commerce-code-block-library.md), and the original Word file is stored at [../assets/tiktok-script-library-original.docx](../assets/tiktok-script-library-original.docx).

## How To Use The Library

Do not copy a template mechanically. Select the script pattern that best proves the product's real value, then adapt language, scene, camera, and proof to the target market.

Default package lock:

- Target market defaults to `US market`.
- Platform defaults to `TikTok US` / `TikTok Shop US` when commerce context fits.
- Runtime defaults to exactly `15 seconds`.
- Viewer-facing language defaults to natural American English.
- Fixed structure defaults to `2s Hook -> 3s Product Reveal -> 4s Demo -> 3s Proof -> 3s CTA`.
- Ignore source-library instructions that ask to confirm country or duration when the user has not requested another market; this skill's default is US 15s.

Every script must pass this value filter before choosing a style:

| Value type | What to prove on screen | Weak version to avoid |
|---|---|---|
| Aesthetic value | Better-looking space, outfit, desk, routine, shelf, face, collection, or setup | Beauty claims with no visible before/after |
| Functional value | Faster, easier, cleaner, safer, more organized, more durable, more comfortable | Feature list without a use moment |
| Add-on value | Bundle, accessory, storage, portability, compatibility, maintenance, gifting, or premium experience | Random props that do not improve use |
| Emotional value | Relief, confidence, pride, calm, satisfaction, control, identity, surprise | Forced excitement or fake urgency |
| Real problem solved | A concrete pain disappears or becomes manageable | Generic "you need this" advertising |

If the product cannot visibly solve a problem in 15 seconds, switch to a lower-risk angle: aesthetic upgrade, organization, giftability, identity, or proof of build quality.

## Diversity And Brand Fit Rules

Use the extracted DOCX library as inspiration, not as a default script engine. Many source templates emphasize price loopholes, stock panic, warehouse chaos, and extreme urgency; apply those only when the offer is real, current, legally usable, and suitable for the product's price tier.

- For a set of five directions, use at least four distinct structure archetypes. Do not make every option a price shock, fake scarcity, or the same UGC reveal with different captions.
- At most one direction should be primarily price-led by default, and only when price or discount evidence exists.
- For high-ticket, premium, professional, giftable, or brand-led products, prioritize ASMR/premium detail, expert/authority, proof/demo, lifestyle, education, review/social proof, or craft/detail patterns.
- For low-ticket impulse products, price and urgency can support the hook, but the product still needs visible value proof beyond "cheap".
- For long-term brand content, favor repeatable pillars: education, proof, lifestyle, craft/detail, trust, community, routine, and gifting.
- Reject any pattern that makes the product look low-quality, hides the real value behind hype, or cannot be repeated without damaging brand trust.

When the user mentions Feishu, 39 code blocks, code-block library, or core commerce modes, read [feishu-commerce-code-block-library.md](feishu-commerce-code-block-library.md). Use its `Core Mode Index` to choose 1-3 source blocks, then adapt them into the current product's selected direction and eight-shot structure.

Extended Feishu modes include:

| Feishu mode | Best fit |
|---|---|
| 鍘熺敓杈句汉/涓绘挱灞曠ず | Fast tactile product desire and native creator recommendation |
| 琛楀ご閲囪/璺汉璇曠敤/绀句細璇佹槑 | Public reaction, impulse validation, and local trust |
| 鏁欑▼婕旂ず/How-to/Demo | Products with clear steps or visible operation |
| 鐥涚偣鍓嶅悗瀵规瘮/缁撴灉杞寲 | Old-way/new-way, transformation, or concrete problem solving |
| 鐭墽鍐茬獊/鎯呯华甯﹁揣 | Emotional conflict, status reversal, or story payoff |
| 璇勮鍥炲/鐢ㄦ埛鍙嶉/璇佽█璇佹槑 | Objection answer, review proof, and skeptical-buyer conversion |
| 闂ㄥ簵璐ф灦/闆跺敭鍙戠幇 POV | Store shelf, checkout, warehouse, or discovery walk-up scenes |
| 鏈嶈璇曠┛/绌挎惌灞曠ず | Apparel, wearables, fit, texture, color, and styling |
| ASMR 鏉愯川缁嗚妭/楂樺鍗曠簿鍝?| Premium material, craft, packaging, quiet luxury, and trust |
| 瀹牸鍒嗛暅/鏁呬簨缂栨帓琛?| Visual board, grid storyboard, and picture-version execution |
| Seedance/Image2/AI 瑙嗛鐢熸垚娴佺▼ | First-frame, Image2, Seedance, and video-model prompt workflows |
| 瑙嗛鎷嗚В/澶嶅埢杩樺師 | Reverse-engineering a reference video into reusable prompts |

## Pattern Picker

| Pattern | Use when | Core sequence |
|---|---|---|
| Native UGC product discovery | Product has tactile details or everyday usefulness | Product in hand -> texture/detail -> function -> satisfied micro-reaction |
| Street interview | Social proof, price shock, or impulse angle matters | Interruption -> quick trial -> shocked reaction -> CTA |
| Immersive tutorial/how-to | Product has a clear operation process | Pain setup -> step-by-step use -> visible result -> CTA |
| Pain replication | Pain point is familiar and visual | Pain scene -> product enters -> quick change -> proof in daily action -> CTA |
| Retail discovery POV | Shelf/store discovery or snack/small goods | Store shelf -> camera walks in -> hand grabs -> inspection -> purchase cue |
| Fashion UGC | Clothing, accessories, wearable goods | Body/fit reveal -> fabric/detail interaction -> styling/use proof -> confidence payoff |
| Short drama commerce | Emotion-led or story-driven category | Conflict -> product as turning point -> reaction -> status/emotion payoff |
| ASMR/premium detail | Texture, material, luxury, storage, tools, desk goods | Quiet setup -> macro material -> slow operation -> premium result |
| Seedance/Image2 story board | Need AI video execution | Clean 9:16 source frames -> locked product -> controlled motion -> no generated text |

## Fixed 15-Second Structure

Use the package default unless the user explicitly overrides it:

```text
2s Hook -> 3s Product Reveal -> 4s Demo -> 3s Proof -> 3s CTA
```

Map it to eight shots:

| Shot | Segment | Job |
|---|---|---|
| S01 | Hook, 0:00-0:02 | Show the pain, desire, disruption, or visual upgrade promise |
| S02 | Product Reveal A, 0:02-0:03.5 | Reveal exact product identity and scale |
| S03 | Product Reveal B, 0:03.5-0:05 | Show verified detail, material, or component |
| S04 | Demo A, 0:05-0:07 | First use action or setup step |
| S05 | Demo B, 0:07-0:09 | Core function or transformation |
| S06 | Proof A, 0:09-0:10.5 | Close-up evidence, result, or objection answer |
| S07 | Proof B, 0:10.5-0:12 | Lifestyle/social/emotional validation |
| S08 | CTA, 0:12-0:15 | Clear offer/action cue without unsupported urgency |

## Native Feel Rules

- Make the video feel like a useful discovery, not a scripted ad.
- Use natural speech, short captions, handheld or creator-camera logic, imperfect but intentional framing, and real use context.
- Avoid generic hype, fake scarcity, over-polished studio lighting, mirror-selfie framing, and machine-translated ad copy.
- Keep subtitles, CTA text, legal text, and price text as post-production overlays; do not ask the image/video model to generate readable text.
- If using urgency, ground it in a verified offer or label it as a creative hypothesis. Do not invent discounts, stock limits, or price errors.

## Language And Market Notes

- Write production explanations in the user's language.
- Write spoken lines, captions, and CTA in the target market's natural register.
- For the default US market, use concise everyday American English and avoid exaggerated livestream phrasing unless requested.
- For Mexico or LatAm, use native Spanish or Spanglish only when the product, audience, and platform fit it.
- Avoid copying fixed personas from the source library. Treat them as examples of tone, not mandatory casting.

## When To Read The Full Extract

Read [tiktok-script-library-full-extract.md](tiktok-script-library-full-extract.md) only when:

- The user requests a specific format from the script library.
- You need exact wording from one of the source workflows.
- The product category matches a source pattern such as fashion, street interview, tutorial, retail discovery, short drama, or Seedance/Image2.
- You need more examples of Spanish/Spanglish hook structure, motion prompts, or story-board wording.