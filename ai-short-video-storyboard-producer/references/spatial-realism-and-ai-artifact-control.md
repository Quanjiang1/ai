Exit code: 0
Wall time: 0.2 seconds
Output:
# Spatial Realism And AI Artifact Control

Use this reference before writing image prompts, video prompts, or production-board panels for product-visible AI commerce video.

## Core Rule

Design physical plausibility before visual polish. A frame with correct product scale, contact, occlusion, and depth beats a beautiful frame with warped hands, floating products, or synthetic lighting.

## Blocking-To-Polish Workflow

1. Write a blocking frame: product scale, support surface, contact point, occlusion order, camera height, and foreground/midground/background.
2. Check the blocking frame against product lock and contact/occlusion lock.
3. Only then write the polished reference-frame prompt.
4. For video prompts, preserve the accepted blocking geometry; move the camera or subject without changing product design, scale, or contact logic.

Do not jump directly from script to polished image when the product touches a person, body, furniture, packaging, liquid, cable, or moving prop.

## Prompt Blocks

### Contact And Occlusion

```text
PHYSICAL CONTACT:
the product rests on [support surface] with its [product area] touching [surface/body area];
[specific hand/prop] is in front of [product edge] and partially occludes it;
the product remains behind [foreground element] and in front of [background element];
visible contact shadow at the support point;
no finger-through-object, no product embedded in skin, no floating product,
no merged material, no duplicated hands, no impossible grip
```

### Environment Depth

```text
ENVIRONMENT DEPTH:
foreground: [partial object or edge close to camera];
midground: [person/product/action plane];
background: [real location elements at distance];
depth cues: perspective lines, contact shadows, mild background softness,
real table/floor plane, consistent shadow direction
```

### Anti-AI Realism

```text
REALISM:
authentic smartphone commerce-video frame, natural mixed lighting,
real skin texture, normal fabric wrinkles, practical household/store props,
slight handheld framing, mild lens distortion, realistic contact shadows,
imperfect but intentional composition;
no glossy CGI, no plastic skin, no waxy face, no over-smoothed product,
no sterile showroom unless specified, no fake readable packaging text,
no warped logo, no floating object
```

## Safe Composition Templates

| Template | Use when | Prompt pattern |
|---|---|---|
| Tabletop demonstration | Product accuracy matters and hand interaction is risky | Product sits on a stable surface; one hand enters from side to press, point, or adjust |
| Hand-near-product operation | Need human presence without complex grip | Hand points near button, hovers beside product, or touches one simple surface |
| Product hero insert | Need exact product shape or branding | Product remains in clean insert/overlay while scene shows use context behind it |
| Split proof shot | Benefit needs before/after or action/result | Shot A shows product safely; Shot B shows result without forcing complex contact |
| Over-shoulder UGC | Need creator authenticity | Person holds phone/camera view; product remains on table or shelf in midground |
| Detail macro | Need button, texture, ingredient, or mechanism | Crop to product detail; avoid full hand wrap around small components |

## Interaction Risk Downgrades

- Two-hand grip -> one hand touching one edge, or product on surface with both hands nearby.
- Product against face/body -> product held away from skin, or use mirror/tabletop/insert.
- Transparent/reflective product -> fixed product angle, controlled reflections, fewer fingers.
- Small product with fingers wrapped around it -> macro detail with fingertips at edges only.
- Moving liquid/cable/hinge -> split into setup shot and result shot.
- Product in crowded environment -> remove unrelated props, keep one foreground and one background layer.

## Environment Depth Checklist

Every environmental frame should answer:

- What is closest to camera?
- Where is the product/action plane?
- What is clearly behind the action?
- Which shadows prove contact?
- Which perspective or blur cue proves distance?
- What practical light source explains the highlights?

## Reject Conditions

Reject or rewrite the prompt when any of these appear in the expected frame:

- Product pierces a hand, arm, body, table, package, wall, or prop.
- Fingers are fused, duplicated, missing, or wrapped impossibly around product parts.
- Product floats without a named support and contact shadow.
- Product scale changes between shots without explanation.
- Environment is a flat blank backdrop when the shot needs real usage context.
- Lighting is evenly synthetic with no practical source or contact shadow.
- Skin, fabric, product surface, or packaging looks waxy, plastic, or overly smooth.
- Generated small text is treated as reliable factual copy.