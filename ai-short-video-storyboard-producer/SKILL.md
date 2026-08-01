Exit code: 0
Wall time: 0.2 seconds
Output:
---
name: ai-short-video-storyboard-producer
description: Use when converting an approved commerce-video strategy into TikTok/Reels/Shorts scripts, fixed eight-shot landscape production boards, native 9:16 AI image/video references, Seedance-style prompts, UGC ads, or visual QA, especially when web-verified product dimensions, product consistency, contact, occlusion, environment depth, or AI-looking artifacts must be controlled.
---

# AI Short-Video Storyboard Producer

Produce visuals from an approved selling strategy. Do not redo market research unless the handoff is missing or contradictory.

## Required Inputs

Confirm or infer conservatively:

- Product image and verified product facts
- Target audience and use occasion
- Main pain, benefit, and proof method
- Product value hypothesis: aesthetic value, functional value, add-on value, emotional value, and the real problem solved
- Selected conversion psychology map: primary lever, secondary lever when useful, buyer barrier reduced, visible proof cue / psychological proof moment, trust/objection cue, CTA psychology, and prohibited psychological shortcut
- Selected first-three-second hook
- Product reveal time
- CTA intent
- Required claims and prohibited claims
- Evidence source for every factual or performance claim
- Platform, market, duration, language, and desired format
- Exact product name/model/SKU when identifiable
- Web-verified product dimensions, materials, components, colorways, included accessories, and source dates
- Product-person interaction risk, support surface, and safe handling assumptions
- Environment realism direction: foreground, midground, background, lighting, and camera texture

If no strategy exists, first run `product-research-viral-hook-strategist`. Do not default from a product image directly into five fictional story worlds.

If the user has provided only a product image and has not selected a video direction yet, route through `product-research-viral-hook-strategist` and present exactly five selectable video directions first. Do not create the picture-board script before the user chooses a direction unless the user explicitly says to choose automatically or produce directly.

If the user has selected one of the five directions, treat that selection as approval. Do not ask for another concept confirmation; proceed directly into the fixed image-board workflow.

A direction selection may be a bare number from `1` to `5`, a short phrase such as `閫?`, `鏂瑰悜3`, `绗笁涓猔, `灏辫繖涓猔, the direction name, or a follow-up request for `鍥剧墖鐗堝叓鍒嗛暅鑴氭湰` after five directions were presented. Treat all of these as approval to produce, not as a prompt to re-explain the workflow.

Do not infer a sensitive claim or exact specification when getting it wrong would materially change the video. Mark it unknown or ask only when necessary.

## Default US 15-Second Lock

Unless the user explicitly specifies another country or runtime, every output must use:

- Market: `US market`.
- Platform: `TikTok US` / `TikTok Shop US` when commerce context fits.
- Runtime: exactly `15 seconds`.
- Language: natural American English for VO, captions, CTA, and consumer-facing copy.
- Structure: `2s Hook -> 3s Product Reveal -> 4s Demo -> 3s Proof -> 3s CTA`.
- Visual context: plausible US homes, cars, apartments, garages, kitchens, bathrooms, closets, offices, retail aisles, suburban/front-door contexts, or creator spaces that fit the product.

Write production explanations in the user's language unless requested otherwise. Write viewer-facing spoken lines, captions, and CTA in natural American English by default. Do not ask for market or duration confirmation unless the user introduces a conflicting requirement.

## Production Modes

Select exactly one mode and state it:

1. `UGC Conversion Ad` - default for commerce short video.
2. `Demonstration Ad` - for products with strong visible proof.
3. `Lifestyle Ad` - for emotional or identity-led products.
4. `Fictional/Comic Commerce Story` - only when explicitly requested or strategically selected.

Use this deliverable layout by default:

- `Fixed eight-shot landscape production board`: a landscape high-density board matching the visual grammar of [assets/fixed-eight-shot-board-reference.png](assets/fixed-eight-shot-board-reference.png). It contains product/style reference, character/prop reference, environment/scene design, exactly eight storyboard panels, lighting/still notes, props/keywords, audio/text, conversion notes, runtime, and CTA bar.
- `Text script and prompts`: use only when the user explicitly requests text-only output or does not want an image board.

Do not create a vertical production-sheet layout unless the user explicitly requests it. Do not mix six-shot and eight-shot requirements.

Always read [references/landscape-production-board.md](references/landscape-production-board.md) when producing the default board or when the user says `鏁呬簨缂栨帓琛╜, `鍏垎闀滄晠浜嬭〃`, `鍒朵綔鎵ц琛╜, `鍙傝€冭繖寮燻, `鍍忚繖寮犲浘`, `妯増鏉垮紡`, or `production board`. Also read [references/tiktok-script-pattern-library.md](references/tiktok-script-pattern-library.md) before selecting script style or hook execution. The board canvas is landscape, but every product, character, environment, detail, and storyboard reference image must first be generated or prepared independently in the target video's native 9:16 aspect ratio, then placed into the landscape board without stretching, deformation, or destructive crop.

## Story Arrangement Board Mode

Use this mode whenever the user asks for `鏁呬簨缂栨帓琛╜, `鍏垎闀滄晠浜嬭〃`, `鍒朵綔鎵ц琛╜, `鍙傝€冭繖寮燻, `鍍忚繖寮犲浘`, `妯増鏉垮紡`, or a board matching the provided reference image.

The required deliverable is a landscape high-density eight-shot story arrangement board, not a plain text table and not only eight independent Seedance frames. It must follow the visual grammar of [assets/fixed-eight-shot-board-reference.png](assets/fixed-eight-shot-board-reference.png):

1. Header: campaign title, 15s TikTok/UGC ad label, product category, `US market`, `15 seconds`, and model/version.
2. Top row: `PRODUCT & STYLE REFERENCE`, `CHARACTER & PROP REFERENCE`, and `ENVIRONMENT & SCENE DESIGN`.
3. Main storyboard: exactly eight panels numbered `01`-`08`, arranged two rows of four, following `2s Hook -> 3s Product Reveal -> 4s Demo -> 3s Proof -> 3s CTA`.
4. Every panel includes a real visual thumbnail, shot headline, camera, motion, light, value proof, VO/subtitle, SFX, and time.
5. Bottom row: lighting/still notes, props/keywords, audio/text, conversion notes, spatial QA, total runtime, and a full-width CTA bar.

Hard rules for this mode:

- Use real photorealistic 9:16 source-frame thumbnails inside the board. Do not use placeholder thumbnails, rough icons, flat diagrams, wireframes, cartoon panels, or UI mockups.
- Board labels, panel numbers, tables, and CTA bars are allowed on the board because it is an approval artifact; they must not appear inside the underlying 9:16 video frames.
- The board must be assembled from real source frames and product references. Do not generate a fake one-piece board and treat its crops as source frames.
- Keep product-visible thumbnails traceable to product-locked 9:16 source frames.
- Do not save generated board files into the user's workspace unless the user explicitly asks to save files. Inline render or default tool storage is acceptable.

If the user asks for both Seedance-ready frames and a story arrangement board, produce or provide the eight real 9:16 source frames first, then assemble the board from those frames.

## Selected Direction To Image Board

When a selected direction arrives from `product-research-viral-hook-strategist`, convert it directly into a picture-version storyboard:

1. Preserve the chosen direction's value combo, conversion psychology map, hook, buyer, proof mechanism, native visual style, Feishu/code-block references, prohibited psychological shortcut, and risk notes.
2. Use the fixed US 15-second order: `2s Hook -> 3s Product Reveal -> 4s Demo -> 3s Proof -> 3s CTA`.
3. Produce exactly eight storyboard shots using the fixed timing map below.
4. For each shot, include the text script, visual action, camera/light/cinematography, contact and occlusion lock, environment depth, realism risk, claim/proof link, 9:16 image prompt, and video prompt.
5. Deliver the eight independent native 9:16 source-frame prompts/assets labeled `S01`-`S08` before or alongside the fixed landscape production board.
6. Produce the fixed eight-shot landscape production-board prompt by default, matching [assets/fixed-eight-shot-board-reference.png](assets/fixed-eight-shot-board-reference.png).

Do not replace the selected direction with a new idea unless the selected direction contradicts verified product facts or claim guardrails. If it contradicts facts, state the conflict and adapt the smallest possible part while preserving the chosen selling angle.

Default response after direction selection: output the complete eight-shot picture-version script immediately. Do not answer with only a strategy summary, only a short shot list, only product analysis, or another set of options. Include:

- Campaign title and selected direction.
- Product fact and claim-status note.
- `US market / TikTok US / 15 seconds` lock.
- Product/value/claim locks.
- Structure archetype, Feishu/code-block reference when used, offer/price evidence status, brand/price-tier fit, and premium/brand guardrails.
- Conversion psychology map and how the eight shots preserve it without exposing internal psychology labels to viewers.
- Fixed 15-second timing map.
- Full eight-shot table.
- Actual visual-reference plan for the picture board: product reference images, character/prop references, environment references, and eight storyboard frame references.
- Eight separate native 9:16 source-frame prompts and, when image generation is available, eight visible realistic `S01`-`S08` reference images.
- Per-shot video prompts.
- A landscape picture-version production board only when it helps review the campaign. The board must use real reference images, not text-only tables, prompt-only output, cartoons, diagrams, wireframes, icons, or placeholder thumbnails.
- Landscape production-board prompt and CTA bar copy.

## Seedance Real Reference Frame Mode

Use this mode whenever the user says `Seedance`, `Seedance 2.0`, `鍗虫ⅵ`, `瑙嗛棣栧抚`, `鐪熷疄9:16鍙傝€冨抚`, `瑙嗛鍙傝€冨抚`, `鐩存帴鍑鸿棰慲, or otherwise indicates the output must be fed directly into an AI video model.

In this mode, the required deliverable is not a designed storyboard board. It is:

1. Eight independent realistic 9:16 reference images labeled `S01`-`S08`, one per storyboard shot.
2. A Seedance-ready video prompt for each reference image.
3. A unified negative prompt and product lock.
4. Optional captions/VO as post-production text only.

Hard rules:

- Generate or provide real photorealistic 9:16 reference frames when an image-generation tool is available.
- Do not substitute a board, collage, layout file, wireframe, sketch, icon scene, flat illustration, cartoon, diagram, or placeholder for a Seedance reference frame.
- Do not create a deterministic fake storyboard image and call it a finished picture-version script.
- Do not save generated outputs into the user's workspace or project folder unless the user explicitly asks for saved files. Render images inline or leave them in the image tool's default internal location.
- If the image tool is unavailable, state that real reference-frame generation is unavailable and provide only the exact prompts; do not fabricate placeholder images.
- If a reference board is also requested, make it secondary and assemble it only from the already generated real 9:16 reference frames.
- Video frames themselves must contain no generated subtitles, CTA text, price text, stickers, tables, story-board labels, panel borders, or prompt text. All text belongs in post-production overlays.

Reject the output and redo it if any frame looks like a placeholder, cartoon, rough diagram, UI board, table, text sheet, or non-photorealistic mockup when the user asked for Seedance-ready pictures.

## Duration And Shot Count

- Use exactly eight storyboard shots for the default production board.
- Default runtime is exactly 15 seconds for the US market. The 15-second structure must follow this order and timing: `2s Hook -> 3s Product Reveal -> 4s Demo -> 3s Proof -> 3s CTA`.
- Map the five-part structure onto the fixed eight storyboard shots:
  - `S01 Hook`: `0:00-0:02` / 2s.
  - `S02 Product Reveal A`: `0:02-0:03.5` / 1.5s.
  - `S03 Product Reveal B`: `0:03.5-0:05` / 1.5s.
  - `S04 Demo A`: `0:05-0:07` / 2s.
  - `S05 Demo B`: `0:07-0:09` / 2s.
  - `S06 Proof A`: `0:09-0:10.5` / 1.5s.
  - `S07 Proof B`: `0:10.5-0:12` / 1.5s.
  - `S08 CTA`: `0:12-0:15` / 3s.
- Keep the order fixed: do not move CTA, proof, or demo beats before product reveal unless the user explicitly overrides the sequence.
- Do not switch to 10 seconds, 20 seconds, 30 seconds, 3 shots, or 6 shots because a source template says so. Use another duration or shot count only when the user explicitly overrides the fixed US 15-second eight-shot format.
- Do not modify dedicated 8-second Feishu blocks into 15 seconds when the user explicitly selects or asks for that 8-second block/mode; preserve the 8-second rhythm and adapt only market, language, product facts, and claims as needed.
- Use fewer or more storyboard shots only when the user explicitly overrides the fixed eight-shot format.

Let the fixed five-part sequence determine the role and timing of the eight shots. Product visibility is not postponed by a rigid story formula.

Create one full production-ready concept by default. Create multiple complete concepts only when the user requests variants; otherwise keep alternatives at hook or opening-shot level.

## First-Three-Second Execution

The first shot must explicitly include:

- First frame
- 0-1 second action
- 1-3 second payoff or open loop
- Spoken line, caption, and sound
- Product reveal timing
- Transition into the main benefit

Ensure the video can be understood with sound off. Keep text short and avoid blocking the product.

## Script Structure

Use the selected strategy and script pattern, typically:

```text
Hook 2s -> Product Reveal 3s -> Demo 4s -> Proof 3s -> CTA 3s
```

Before writing the eight-shot table, choose one primary script pattern from [references/tiktok-script-pattern-library.md](references/tiktok-script-pattern-library.md), such as native UGC discovery, street interview, immersive tutorial, pain replication, retail discovery POV, fashion UGC, short drama commerce, ASMR/premium detail, or Seedance/Image2 story board. If the selected direction includes Feishu/code-block references, inspect the relevant entries in [references/feishu-commerce-code-block-library.md](references/feishu-commerce-code-block-library.md) and adapt their structure into the eight-shot board. Convert any non-US market, Spanish/LatAm copy, variable duration, 6-shot, or 3-shot source block into the fixed US 15-second structure, but keep dedicated 8-second Feishu blocks at 8 seconds when explicitly selected. The chosen pattern must serve the product's real value, not override it.

For every concept, state which value is being sold and how it appears on screen:

| Value | Requirement |
|---|---|
| Aesthetic value | Show a visible upgrade in look, setup, outfit, shelf, desk, face, or routine |
| Functional value | Show the product making a task easier, faster, cleaner, safer, more organized, or more comfortable |
| Add-on value | Show bundle/accessory/storage/compatibility/gift/premium benefit only when real |
| Emotional value | Show relief, confidence, pride, calm, satisfaction, control, surprise, or identity without fake acting |
| Real problem solved | Show the pain disappearing, reducing, or becoming easier to manage |

If a value cannot be shown, do not make it the main selling angle.

## Creative Claim Guardrails

Commerce scripts may use moderate exaggeration to make the viewer feel the problem and payoff, but every factual or regulated claim must stay evidence-backed.

Allowed without product-specific evidence:

- Subjective sensory language: `smells fresher`, `feels cleaner`, `less stuffy`, `more comfortable`, `space feels reset`.
- Reaction-based proof: the person stops spraying, relaxes after entering the car, stops grimacing, or prefers the new routine.
- Old-way/new-way contrast: repeated spraying feels annoying; a placed gel jar feels simpler and more premium.

Evidence-required and otherwise prohibited:

- Antibacterial, germ-killing, disinfecting, sanitizing, air purification, formaldehyde/VOC removal, allergen removal, smoke removal, medical relief, anti-nausea, motion-sickness treatment, or any measurable health/safety/performance result.
- Do not show lab tests, bacteria animations, medical relief scenes, air-purifier-style particle removal, or treatment outcomes unless the production handoff includes traceable supporting evidence.

When the desired selling idea is high-risk, rewrite it into a sensory or emotional claim:

| High-risk wording | Use instead when unverified |
|---|---|
| Kills germs / disinfects | Smells fresher and feels cleaner |
| Purifies the air | Freshens the space / helps with unwanted odors |
| Treats motion sickness | Makes the car feel less stuffy and more comfortable |
| Removes all odors | Helps reduce that stale smell |

Put the approved wording in VO, captions, CTA, image prompts, and board notes. Do not let generated visuals imply a stronger claim than the script says.

## Offer And Brand Tone Guardrails

Preserve the selected direction's brand/price-tier fit when turning strategy into an eight-shot board.

- Do not add `price glitch`, `secret loophole`, fake markdown, fake scarcity, countdown panic, or unverified discount language during storyboard production.
- If the chosen direction is not price-led, do not introduce price-led CTA copy, coupon visuals, bargain props, or cheap-looking urgency.
- If the product is high-ticket, premium, professional, giftable, or brand-led, use trust-building visuals: materials, detail, service, craftsmanship, expert use, organized environment, social proof, or premium lifestyle context.
- Avoid bargain-bin visual cues for premium products: cluttered discount tables, flashing sale stickers, chaotic yelling faces, exaggerated shock expressions, cheap props, fake warehouse clearance, or overly loud typography.
- The CTA tone must match the product tier: premium products use confident, calm, value-led CTA; low-ticket impulse products may use stronger urgency only when the offer is verified.
- Keep the five-part runtime structure, but vary internal pacing, scene logic, proof method, and camera language so the board does not feel like the same video with a different caption.
- Treat the selected structure archetype as a creative constraint. Preserve its viewing logic across the eight panels instead of turning every direction into the same pain -> reveal -> demo -> CTA template.
- Use price tier to choose production texture: low-ticket impulse can be quicker and more spontaneous; mid-ticket value should show practical proof; high-ticket or brand-led products need calmer pacing, cleaner blocking, credible environments, and trust-led copy.
- Long-term brand content must leave the product more desirable after repeat viewing. Favor education, craft/detail, proof, lifestyle, trust, community, and repeat-use scenes over one-off exploit hooks.
- Rewrite the board if the eight panels rely on fake price drama, make the product look cheap, repeat the same proof beat, or contradict the selected brand/price-tier fit.

For each shot specify:

| Field | Requirement |
|---|---|
| Time | Start/end and duration |
| Job | Hook, product reveal, demo, proof, objection, payoff, or CTA |
| Visual/action | Person, product, and environment action |
| Camera/light | Framing, movement, light, and visual emphasis |
| Cinematography | Camera height, lens/framing, light source, depth plan, product highlight, and motion purpose |
| Audio/text | Spoken line, caption, SFX |
| Product visibility | Full, partial, detail, or absent with reason |
| Contact/occlusion | Support surface, contact points, front/back layering, and prohibited intersections |
| Environment depth | Foreground, midground, background, and visible depth cues |
| Realism risk | Low, medium, or high risk plus any downgrade, split-shot, or compositing plan |
| Claim/proof link | Which approved claim the shot demonstrates and how |
| Conversion psychology | Which primary lever, buyer barrier, visible proof cue / psychological proof moment, trust/objection cue, or CTA psychology the shot supports, plus which psychological shortcut is prohibited |
| Structure/brand fit | How the shot preserves the selected structure archetype, Feishu/code-block reference if used, offer/price evidence status, CTA tier, and brand/price-tier tone |
| Image prompt | Still reference-frame prompt |
| Video prompt | Start frame, motion, camera, change, duration |

## Product Accuracy

Before writing image or video prompts, create `WEB PRODUCT DETAIL LOCK`, `PRODUCT LOCK`, `CONTACT/OCCLUSION LOCK`, `ENVIRONMENT DEPTH LOCK`, `REALISM LOCK`, and `PROFESSIONAL NATIVE CINEMATOGRAPHY LOCK` using [references/product-and-visual-locks.md](references/product-and-visual-locks.md), [references/spatial-realism-and-ai-artifact-control.md](references/spatial-realism-and-ai-artifact-control.md), and [references/professional-cinematography-standards.md](references/professional-cinematography-standards.md).

If the exact product, model, or SKU is identifiable, browse the web before production to verify product dimensions, materials, components, accessories, color, controls, labels, and usage direction. Prefer brand pages, manuals, official listings, retailer listings, and traceable product pages. Cite source URLs and access dates in the product detail ledger. Do not borrow dimensions or features from a similar variant.

Priority:

```text
Web-verified product identity, dimensions, and scale
> product factual accuracy
> product consistency
> real product value proof
> claim compliance
> professional native cinematography
> selling clarity
> visual beauty
> creative novelty
```

Use conservative angles, split shots, or scene-plus-product compositing when generation would alter the product, merge the product into hands, flatten the environment, or create a glossy AI look. Never accept a beautiful but incorrect, warped, physically impossible, or wrong-model product frame.

## Visual References And Prompts

- Generate one independent native 9:16 reference frame per shot before assembling the default landscape board.
- Generate or prepare every source reference image in native 9:16: product hero, product detail, character, prop, environment, layout/blocking, and all eight storyboard frames.
- Deliver and label the eight 9:16 storyboard source frames separately as `S01` through `S08` before or alongside the landscape board.
- For every product-visible frame, first design a blocking frame that verifies product scale, support surface, contact point, occlusion order, and foreground/midground/background depth before producing a polished reference frame.
- Keep every source reference frame as a separate deliverable asset; do not generate the board as one image and treat cropped board panels as the source frames.
- When placing 9:16 sources into landscape board cells, use fit-with-padding, controlled masks, or safe-area preview crops. Never stretch width/height, squash, bend, redraw, or relight the product to fit a cell.
- Match each frame to its shot job; do not repeat one generic product image.
- Use authentic market-specific environments, casting, behavior, language, and props.
- For the default US market, use natural American English and recognizable US daily-life contexts. Do not leave Mexico/LatAm personas, Spanish voiceover, or regional slang in the final script unless the user explicitly asks for that market.
- Use the complexity budget in [references/spatial-realism-and-ai-artifact-control.md](references/spatial-realism-and-ai-artifact-control.md); downgrade high-risk hand/product interactions unless the exact interaction is necessary to prove the benefit.
- Keep people, hands, support surfaces, perspective, shadows, occlusion, and product contact physically plausible.
- Prefer safe composition templates: tabletop demonstration, hand-near-product operation, product hero insert, pointing gesture, or reference-product compositing when direct grip would risk warping or intersection.
- Put exact product locks in every product-visible image and video prompt.
- Put contact, occlusion, depth, and anti-AI-realism constraints in every product-visible or person-visible prompt.
- Put professional native cinematography constraints in every polished image/video prompt: motivated light, intentional framing, product-readable edges, real texture, depth, purposeful camera movement, and native creator-camera feel.
- Treat generated small text as unreliable; add precise captions in post-production.
- Separate generated visual prompts from post-production overlays, captions, legal text, and CTA.
- When producing multiple test variants, keep downstream shots stable if the test is intended to isolate the hook.

## Fictional/Comic Mode

Only in this mode:

1. Offer up to five story directions if the user has not selected one.
2. Turn the product into a meaningful story device.
3. Preserve the approved hook, selling angle, and product proof.
4. Lock character and scene continuity.
5. Use an eight-shot structure by default.

Entertainment must still lead to a credible product benefit.

## Default Deliverable

1. Production mode and strategy handoff
2. Web product detail ledger with source URLs/dates, dimensions, materials, components, accessories, and unknowns
3. Product value proof map: aesthetic, functional, add-on, emotional, and real problem solved
4. Conversion psychology map: primary lever, secondary lever when useful, buyer barrier reduced, visible proof cue / psychological proof moment, trust/objection cue, CTA psychology, and prohibited psychological shortcut
5. Selected script-library pattern plus Feishu/code-block reference when used, and why it fits the product
6. Product lock, contact/occlusion lock, environment depth lock, realism lock, professional native cinematography lock, and claim guardrails
7. Fixed eight-shot duration map
8. Executable eight-shot table with contact, occlusion, depth, cinematography, conversion psychology, and realism-risk fields
9. Blocking-frame notes before polished 9:16 reference-frame prompts
10. Eight independent 9:16 storyboard source-frame prompts/assets labeled `S01`-`S08`
11. Per-shot video prompts when requested or needed
12. Fixed eight-shot landscape production-board prompt and assembled board by default
13. Post-production overlay list
14. QA checklist

## QA

Check:

- First frame has stop power and audience relevance.
- Market and runtime are locked to `US market / TikTok US / 15 seconds` unless explicitly overridden.
- First three seconds preserve the selected hook hypothesis.
- Product connects naturally to the hook.
- Main benefit is visibly proved, not merely claimed.
- The selected conversion psychology map is preserved: the hook carries the primary lever, the demo/proof reduces the named buyer barrier with visible proof, the CTA matches the chosen CTA psychology, and the prohibited psychological shortcut is not introduced downstream.
- No fake urgency, fake scarcity, fake authority, invented reviews, hidden discounts, unsupported fear, or product inaccuracy is added in shot design, overlay copy, props, packaging, reviews, or CTA.
- The script pattern supports the product's real value and does not force a mismatched template.
- Feishu/code-block references, when used, are adapted into product-accurate eight-shot execution rather than copied as text-only prompts.
- The board preserves the chosen structure archetype and does not collapse into the same generic video pattern used for every product.
- Price, discount, loophole, or urgency appears only when verified and brand-appropriate.
- High-ticket, premium, professional, giftable, or brand-led products do not look cheap, desperate, or low-trust.
- If the chosen direction is not price-led, no downstream shot, overlay, CTA, prop, environment, or voice line turns it into a price-led ad.
- High-ticket and brand-led boards include at least two trust-building proof cues, such as material detail, expert use, service/warranty context, creator credibility, customer reaction, durability proof, or premium routine.
- Eight panels vary their opening image, proof beat, camera language, environment role, and CTA logic enough to feel like a designed campaign rather than a recycled template.
- At least one of aesthetic value, functional value, add-on value, emotional value, or real problem solved is shown concretely on screen.
- Every factual claim is approved and linked to evidence; unknown claims are omitted.
- Product shape, color, components, logo, scale, and usage remain consistent.
- Product dimensions, detail claims, accessories, and usage direction match web-verified sources or are explicitly marked unknown.
- No other model, variant, colorway, accessory set, or generic substitute is silently used.
- Product is physically integrated into the scene.
- Product never intersects hands, body, furniture, surfaces, packaging, or props in impossible ways.
- Contact points, occlusion order, and support surfaces are named for every product-visible shot.
- Each scene has a readable foreground, midground, background, and depth cue unless a clean product insert is intentionally used.
- Frames avoid glossy CGI, plastic skin, over-smoothed surfaces, floating objects, fake packaging text, and sterile showroom lighting unless strategically required.
- Visuals meet professional native cinematography standards: motivated light, intentional framing, product-readable detail, depth, real texture, and purposeful camera movement.
- Native feel is preserved: useful discovery, natural speech, real use context, and no generic ad gloss.
- All source reference images are native 9:16 before board assembly.
- The default board contains exactly eight storyboard panels numbered `01` through `08`.
- The board follows the fixed top-reference, eight-panel storyboard, bottom-production-row, runtime, and CTA-bar layout.
- Board placement never stretches, squashes, or redraws a product-visible 9:16 source image.
- Spoken lines and captions are native, short, and compliant.
- Every shot has a conversion or narrative job.
- CTA matches the platform and does not make unsupported urgency claims.
- The default deliverable is one coherent landscape high-density board.
- Every storyboard source frame remains an independent native 9:16 asset with no stretch, horizontal generation, or destructive crop.