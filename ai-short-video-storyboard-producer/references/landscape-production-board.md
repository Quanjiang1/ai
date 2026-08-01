Exit code: 0
Wall time: 0.2 seconds
Output:
# Fixed Eight-Shot Landscape Production Board

Use this format by default for visual-production delivery. It is a commercial storyboard production sheet containing product references, casting, scenes, exactly eight storyboard panels, production notes, conversion notes, runtime, and CTA. Use [../assets/fixed-eight-shot-board-reference.png](../assets/fixed-eight-shot-board-reference.png) as the layout/style reference when available.

## Purpose

Use the board as a production overview and approval artifact. Do not confuse the board's landscape canvas with the final video's aspect ratio.

- Board canvas: landscape, normally 16:9 or 16:10.
- Final short-video composition: normally native 9:16.
- The deliverable is a picture-version board: it must show visible product/style, character/prop, environment, and eight storyboard reference images. A text table, shot list, or prompt list alone is not sufficient when the user asks for a picture-version script.
- When the user says `鏁呬簨缂栨帓琛╜, `鍏垎闀滄晠浜嬭〃`, `鍒朵綔鎵ц琛╜, `鍙傝€冭繖寮燻, `鍍忚繖寮犲浘`, or provides the cigar-storage reference image, this file is the required output contract.
- If the user asks for Seedance, video-model reference frames, true pictures, real reference images, or direct video generation input, deliver the eight independent realistic 9:16 source frames first. A landscape board is only secondary and must be assembled from those real source frames.
- Generate every product, character, prop, environment, detail, layout/blocking, and storyboard reference image independently as a native 9:16 source before placing it into the board.
- Keep the independent 9:16 source images unchanged; fit them into board cells with padding, source-safe masks, or labeled previews, never horizontal stretching, vertical squashing, redrawing, or destructive cropping.
- Do not generate landscape storyboard frames and later crop them into 9:16.
- Do not generate the whole board as one image and treat crops from it as source references.
- Add small labels, notes, and CTA during deterministic post-production layout; do not rely on an image model to render dense text.
- Do not use placeholders, rough icons, flat diagrams, wireframes, UI blocks, cartoons, or synthetic board sketches as finished visual references. If image generation is unavailable, provide prompts only and state that real reference images were not generated.

## Reference Image Contract

Match the user's provided cigar-storage board at the structural level:

- White background, thick black outer border, thin black internal grid, red numbered section headers, red circular storyboard numbers.
- Header height is compact: left side campaign title and ad/category tag; right side market, runtime, and model/version.
- Top reference row has exactly three large sections:
  - `1. PRODUCT & STYLE REFERENCE`: product hero, product detail crops, material/finish/component notes, verified or unknown dimensions.
  - `2. CHARACTER & PROP REFERENCE`: character states, product interaction beats, and only relevant props.
  - `3. ENVIRONMENT & SCENE DESIGN`: hero environment, alternate placements, top-down blocking or layout map, scale/clearance notes.
- Main section title is `4. STORYBOARD - [CAMPAIGN RUN]`.
- Storyboard contains exactly eight panels in two rows of four. Each panel has one real thumbnail on top and a compact production-note block below.
- Bottom production row contains numbered sections `5`-`10`: lighting/still notes, props/keywords, audio/text, conversion notes, spatial QA, and total runtime.
- Final full-width bottom CTA bar is required when the ad has a CTA.
- Do not output a vertical story sheet when this reference is requested.
- Do not replace the board with only independent Seedance frames unless the user asks specifically for direct Seedance input instead of the story arrangement board.

## Fixed Board Structure

### Header

- Left: campaign title, duration/platform ad type, product category, and format tag.
- Right: target market, total runtime, production/video model, and version when relevant.
- Show the fixed 15-second structure when applicable: `2s Hook / 3s Product Reveal / 4s Demo / 3s Proof / 3s CTA`.

### Top Reference Row

1. `PRODUCT & STYLE REFERENCE`
   - Native 9:16 product hero views, product detail references, materials, verified dimensions/scale anchors, components, included accessories, product lock, and source/date notes.
   - Include exact product footprint/dimensions from web verification when available; do not invent product measurements.
2. `CHARACTER & PROP REFERENCE`
   - Native 9:16 character beats, wardrobe, hand interaction, contact/occlusion lock, and only relevant props.
3. `ENVIRONMENT & SCENE DESIGN`
   - Native 9:16 environment references, alternate placements, foreground/midground/background layers, layout/blocking map, camera positions, light direction, and scale relationships.
   - Include a top-down or blocking diagram only as a layout aid; do not let it replace native 9:16 scene references.

### Main Storyboard

- Use exactly eight panels numbered `01` through `08`.
- Arrange panels in reading order as two rows of four, matching the reference board style unless the target canvas requires a minor spacing adjustment.
- Use this default 15-second panel map:

| Panel | Segment | Time |
|---|---|---:|
| `01` | Hook | `0:00-0:02` |
| `02` | Product Reveal A | `0:02-0:03.5` |
| `03` | Product Reveal B | `0:03.5-0:05` |
| `04` | Demo A | `0:05-0:07` |
| `05` | Demo B | `0:07-0:09` |
| `06` | Proof A | `0:09-0:10.5` |
| `07` | Proof B | `0:10.5-0:12` |
| `08` | CTA | `0:12-0:15` |

- Keep the five segments in order: Hook, Product Reveal, Demo, Proof, CTA.
- Each panel includes:
  - Number
  - 9:16 source-frame preview or safe preview crop labeled `S01`-`S08`
  - Short shot headline
  - `CAMERA`
  - `MOTION`
  - `LIGHT`
  - `CINEMATOGRAPHY`
  - `VALUE PROOF`
  - `CONTACT`
  - `OCCLUSION`
  - `DEPTH`
  - `REALISM RISK`
  - `VO/SUB`
  - `SFX`
  - `TIME`
- Make the first-three-second panels visually prominent enough to review the hook.
- Preserve each independent native 9:16 source frame and its safe areas inside every preview.
- Never stretch, squash, bend, redraw, or relight the product to fit the panel. Use padding or safe preview crop instead.

### Bottom Production Row

5. `LIGHTING / VIDEO / STILL NOTES`
6. `PROPS & KEYWORDS`
7. `AUDIO / TEXT`
8. `CONVERSION NOTES`
9. `SPATIAL QA`
10. `TOTAL RUNTIME`

Finish with a full-width CTA bar when the approved strategy calls for a CTA. Keep CTA text deterministic and added in layout, not generated inside image frames.

## Conversion Notes

Always include:

- First-frame mechanism
- First-three-second hypothesis
- Product reveal time
- Primary proof moment
- Objection-answer moment
- CTA timing
- Test variable and success metric
- Product support surface, contact/occlusion risk, and downgrade plan if relevant
- Web-verified product dimension/detail source status and any unknowns
- Confirmation that timing follows `2s Hook / 3s Product Reveal / 4s Demo / 3s Proof / 3s CTA`
- Selected script-library pattern and the product value it proves
- Selected structure archetype and how the eight panels avoid becoming repetitive
- Offer/price evidence status, including any prohibited price, discount, loophole, scarcity, or urgency language
- Brand/price-tier fit, CTA tier, and premium/high-ticket tone protections
- Professional native cinematography notes: light source, framing logic, depth, camera movement, and product highlight

## Visual Style

- White background, clear black grid, compact but readable hierarchy.
- Use one accent color for numbering and section headings.
- Use red section numbers and red circular storyboard panel numbers when matching the reference board.
- Give imagery priority over decorative elements.
- Keep labels concise; avoid unreadably dense paragraphs.
- Make the board look professionally directed: every preview should have motivated light, product-readable detail, foreground/midground/background depth, and an intentional camera choice.
- Use authentic photographic frames for UGC, demonstration, and lifestyle modes.
- Use realistic camera texture: natural mixed lighting, contact shadows, mild lens distortion, normal skin/fabric texture, and practical props.
- Avoid glossy CGI, plastic skin, over-smoothed surfaces, floating products, sterile showroom lighting, and fake readable package text unless intentionally required.
- For Seedance-ready output, every source frame must be photorealistic and video-feasible; no storyboard-card borders, panel numbers, labels, captions, CTA bars, UI grids, or table fields may appear inside the actual 9:16 frame.
- Use illustrated frames only for explicitly selected fictional/comic mode.

## Board QA

- Board contains all required sections without duplicated or contradictory information.
- Storyboard sequence matches the approved script and timestamps.
- Hook panels clearly communicate the first-three-second hypothesis.
- The selected script-library pattern is named and fits the product value.
- The selected structure archetype, offer/price evidence status, brand/price-tier fit, and CTA tier are visible in the board notes.
- The board does not rely on fake price loopholes, fake markdowns, fake scarcity, or discount-first framing unless a verified offer explicitly supports that route.
- Premium, high-ticket, professional, giftable, or brand-led products are not shown with bargain-bin environments, cheap props, desperate captions, chaotic discount tables, or low-trust urgency.
- The eight storyboard panels vary framing, proof mechanism, environment role, and emotional beat enough to avoid a repeated-template feel.
- Product value is visible: aesthetic upgrade, functional proof, add-on benefit, emotional payoff, or real problem solved.
- Product views and storyboard frames use the same product lock.
- Product dimensions, materials, components, accessory count, and variant match the web product detail lock.
- Each product-visible panel names the support surface, contact point, occlusion order, and realism risk.
- Environmental panels show foreground, midground, background, and at least one depth cue.
- Panels meet professional native cinematography standards without losing TikTok/UGC native feel.
- All frames preserve target-video composition and safe areas.
- Every product, character, environment, detail, and storyboard preview can be traced back to an independent native 9:16 source image.
- The board contains exactly eight storyboard panels numbered `01` to `08`.
- The storyboard timing follows the fixed 15-second order: 2s Hook, 3s Product Reveal, 4s Demo, 3s Proof, 3s CTA.
- Small text is added in layout and remains readable at delivery resolution.
- Conversion notes describe a measurable test, not generic marketing language.
- If the user requested Seedance-ready pictures, the board is invalid unless eight independent realistic 9:16 source frames already exist or are provided inline.