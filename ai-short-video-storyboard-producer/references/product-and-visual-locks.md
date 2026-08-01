Exit code: 0
Wall time: 0.2 seconds
Output:
# Product And Visual Locks

## Web Product Detail Lock

Complete before any product-visible prompt when the exact product can be identified or when the output names product details, dimensions, accessories, materials, or model-specific features.

| Field | Content |
|---|---|
| Exact product identity | Brand, product name, model, SKU, variant, colorway, and confidence |
| Research date | Date the product details were checked |
| Source priority | Brand site, manual/spec sheet, official listing, retailer listing, review only if traceable |
| Dimensions | Width, depth, height, weight, capacity, screen/door/drawer size, cable length, or category-relevant measures |
| Materials/finish | Shell, fabric, glass, wood, metal, plastic, coating, texture, and color |
| Components | Doors, drawers, handles, ports, buttons, hinges, wheels, trays, shelves, labels, accessories, and quantities |
| Included accessories | Exact included items; separate optional accessories from bundled items |
| Usage direction | How the product opens, sits, mounts, connects, holds, dispenses, folds, charges, or operates |
| Source URLs/dates | URL or traceable source title plus access date for each important detail |
| Unknowns | Details not visible or not verified; do not invent them |
| Variant guardrail | Similar models, sizes, colors, and accessory bundles that must not be substituted |

If sources disagree, use the most primary source and state the conflict. If no reliable source verifies dimensions or model details, write `unverified` and avoid exact measurements, labels, or claims in the board.

Append to every product-visible prompt:

```text
WEB PRODUCT DETAIL LOCK:
use the exact product model and variant verified from [source/date];
preserve verified dimensions and proportions: [W x D x H or relevant measures];
preserve verified materials, finish, components, accessories, controls, and branding placement;
do not substitute a similar model, different size, different colorway, missing accessory,
extra accessory, generic product, or invented component;
unverified details must remain visually neutral and unlabeled
```

## Product Lock

Complete before producing product-visible frames:

| Field | Content |
|---|---|
| Product identity | Exact model or clearly labeled category inference |
| Shape | Overall silhouette and front/side anchors |
| Color/material | Visible colors, finish, transparency, texture |
| Real-world scale | Micro, small handheld, tabletop, human-scale, or larger |
| Proportions | Height-to-width relationship and important component ratios |
| Components | Count, positions, connections, buttons, handles, wheels, ports, lids, accessories |
| Branding | Logo/label position; describe unreadable text conservatively |
| Usage direction | How people hold, place, connect, or operate it |
| Unknowns | Details that must not be invented |
| Do not change | Shape, scale, proportions, component relationships, color, and usage |

Append to every product-visible prompt:

```text
PRODUCT LOCK:
preserve the exact product silhouette, color, material, component count,
component positions, component ratios, real-world scale, usage direction,
and branding placement from the reference image;
camera position and crop may change, product design and dimensions may not;
no oversized product, no miniature product, no warped geometry,
no invented accessories, no duplicated components, no logo distortion,
no stretched product, no squashed product, no changed aspect ratio,
no wrong model, no wrong variant, no mismatched accessory bundle
```

## Scene Integration Lock

- Match perspective, contact point, occlusion, shadow direction, color temperature, grain, and sharpness.
- Keep scale correct relative to hands, furniture, vehicles, rooms, and environment.
- Prefer a compatible product angle over forcing an impossible viewpoint.
- Use detail shots or a product anchor inset when a full product cannot be integrated credibly.

## Contact/Occlusion Lock

Complete for every product-visible shot, even when no hand touches the product:

| Field | Content |
|---|---|
| Product support | Hand, tabletop, wall, shelf, hook, floor, packaging, stand, or no-touch insert |
| Contact point | Exact product edge/surface and exact body/surface area that touches it |
| Occlusion order | What is in front, what is behind, and which edges are partially hidden |
| Grip or operation | Pinch, palm support, button press, pointing, sliding, pouring, placing, or no direct grip |
| Shadow/contact cue | Contact shadow, cast shadow direction, pressure mark, reflection, or surface indentation |
| Forbidden intersections | Fingers through product, product embedded in palm, floating object, duplicated hands, merged props |
| Fallback composition | Tabletop demo, hand-near-product, product insert, split shot, or composited product anchor |

Append to every prompt with product-person or product-surface interaction:

```text
CONTACT/OCCLUSION LOCK:
the product is supported by [support];
the only contact point is [specific product area] touching [specific hand/body/surface area];
[foreground object/body part] is in front of [product edge], [background element] remains behind;
show a real contact shadow at the touch point;
no fingers passing through the product, no product embedded in the hand,
no floating product, no merged skin and product material,
no duplicated hands, no impossible grip, no hidden extra components
```

## Interaction Complexity Budget

Choose the simplest composition that proves the shot's job.

| Risk | Examples | Rule |
|---|---|---|
| Low | Product on table, product insert, hand pointing near product, person behind product | Default for factual product shots |
| Medium | One hand pressing a visible button, placing product on surface, simple grip with few occlusions | Use only with explicit contact/occlusion lock |
| High | Two hands gripping, transparent or reflective product, product against face/body, fingers wrapped around small parts, liquids, cables, fast motion | Split into multiple shots, use a safer angle, or use compositing unless the interaction is essential |

High-risk shots must include a fallback. If the product design, hand anatomy, scale, or contact point changes, reject the frame even when the composition looks attractive.

## Character Lock

When continuity matters, repeat age range, face anchors, hair, outfit, accessories, body type, demeanor, and identifying detail in every applicable prompt.

## Scene Lock

When continuity matters, repeat location, layout, time, palette, light direction, recurring props, and product placement logic.

## Environment Depth Lock

Complete for every scene that is not a clean product insert:

| Layer | Content |
|---|---|
| Foreground | Partial object, table edge, hand edge, packaging edge, doorway, shelf edge, or soft occluder |
| Midground | Product and primary action plane |
| Background | Real room/store/street elements with distance and scale |
| Depth cues | Perspective lines, contact shadows, cast shadows, lens blur, atmospheric softness, reflections, or floor/table plane |
| Light logic | Key light direction, fill level, color temperature, and practical light source |

Avoid empty showroom space unless the strategy specifically calls for it. A realistic environment should feel lived-in but controlled, with props that explain use context rather than decorate randomly.

## Realism Lock

Use photographic imperfections that fit the platform and market:

- Handheld smartphone or creator-camera framing when the format is UGC.
- Natural mixed lighting, real contact shadows, mild lens distortion, and small exposure variation.
- Real skin texture, normal fabric wrinkles, fingerprints, dust, surface wear, and non-perfect product reflections when appropriate.
- Compression-friendly contrast and readable product edges.

Avoid:

- Glossy CGI, plastic skin, waxy faces, over-smoothed surfaces, synthetic depth of field, sterile showroom lighting, floating objects, fake packaging text, warped logos, and unrealistically clean props.

## Frame QA

- Correct shape, color, material, branding, components, and count
- Correct verified dimensions, proportions, model, variant, and accessory bundle
- Correct product-to-person and product-to-environment scale
- No product size drift between frames
- Named support surface, named contact point, plausible occlusion order, and visible contact shadow
- Realistic hands, contact, perspective, shadows, and occlusion
- Foreground, midground, background, and at least one depth cue are visible when the shot is environmental
- Realistic camera texture and lighting; no glossy CGI or over-smoothed AI look
- No packaging gibberish presented as trustworthy text
- No duplicated faces, products, or components
- No unsupported visual claim

