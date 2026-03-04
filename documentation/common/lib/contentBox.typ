#let contentBox(
  fill: luma(240),
  inset: 16pt,
  radius: 4pt,
  ..content
) = {
  block(
    width: 100%,
    fill: fill,
    inset: inset,
    radius: radius,
    ..content,
  )
}
