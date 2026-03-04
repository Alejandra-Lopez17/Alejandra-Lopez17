#import "theme.typ": theme

#let layoutA(
  content: [],
) = {
  set page(
    width: 13.3333in,
    height: 7.5in,
    background: image("./slide-layouts/oneV2.svg"),
    margin: (top: 1.5in, bottom: 1in, left: 1in, right: 1in),
  )
  show heading.where(level: 1): it => [
    #set text(size: 32pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 2): it => [
    #set text(size: 28pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 3): it => [
    #set text(size: 24pt, fill: theme.primary, weight: "bold")
    #it
  ]
  set text(
    size: 20pt,
    font: ("Manrope"),
    weight: "light",
  )
  [
    #content
  ]
}

#let layoutATwoCols(
  contentLeft: [],
  contentRight: [],
) = {
  set page(
    width: 13.3333in,
    height: 7.5in,
    background: image("./slide-layouts/oneV2.svg"),
    margin: (top: 1.5in, bottom: 1in, left: 1in, right: 1in),
  )
  show heading.where(level: 1): it => [
    #set text(size: 32pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 2): it => [
    #set text(size: 28pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 3): it => [
    #set text(size: 24pt, fill: theme.primary, weight: "bold")
    #it
  ]
  set text(
    size: 20pt,
    font: "Manrope",
    weight: "light",
  )
  [
    #grid(
      columns: (1fr, 1fr),
      gutter: 0.5in,
      contentLeft,
      contentRight,
    )
  ]
}

#let layoutATwoColsWithTitle(
  title: lorem(8),
  contentLeft: [],
  contentRight: [],
) = {
  set page(
    width: 13.3333in,
    height: 7.5in,
    background: image("./slide-layouts/oneV2.svg"),
    margin: (top: 1.5in, bottom: 1in, left: 1in, right: 1in),
  )
  show heading.where(level: 1): it => [
    #set text(size: 32pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 2): it => [
    #set text(size: 28pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 3): it => [
    #set text(size: 24pt, fill: theme.primary, weight: "bold")
    #it
  ]
  set text(
    size: 20pt,
    font: "Manrope",
    weight: "light",
  )
  [
    = #title

    #grid(
      columns: (1fr, 1fr),
      gutter: 0.5in,
      contentLeft,
      contentRight,
    )
  ]
}

#let layoutBTwoCols(
  contentLeft: [],
  contentRight: [],
) = {
  set page(
    width: 13.3333in,
    height: 7.5in,
    background: image("./slide-layouts/oneV1.svg"),
    margin: (top: 1.5in, bottom: 1in, left: 1in, right: 1in),
  )
  show heading.where(level: 1): it => [
    #set text(size: 32pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 2): it => [
    #set text(size: 28pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 3): it => [
    #set text(size: 24pt, fill: theme.primary, weight: "bold")
    #it
  ]
  set text(
    size: 20pt,
    font: "Manrope",
    weight: "light",
  )
  [
    #grid(
      columns: (1.4fr, 0.5fr, 1fr),
      gutter: 0.5in,
      contentLeft,
      [],
      contentRight,
    )
  ]
}

#let layoutC(
  title: lorem(8),
  content: [],
) = {
  set page(
    width: 13.3333in,
    height: 7.5in,
    background: image("./slide-layouts/twoV2.svg"),
    margin: (top: 0.5in, bottom: 1in, left: 1in, right: 1in),
  )
  show heading.where(level: 1): it => [
    #set text(size: 32pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 2): it => [
    #set text(size: 28pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 3): it => [
    #set text(size: 24pt, fill: theme.primary, weight: "bold")
    #it
  ]
  set text(
    size: 20pt,
    font: "Manrope",
    weight: "light",
  )
  [
    = #title
    #v(24pt)
    #content
  ]
}

#let layoutCTwoColsWithTitle(
  title: lorem(8),
  contentLeft: [],
  contentRight: [],
) = {
  set page(
    width: 13.3333in,
    height: 7.5in,
    background: image("./slide-layouts/twoV2.svg"),
    margin: (top: 0.5in, bottom: 1in, left: 1in, right: 1in),
  )
  show heading.where(level: 1): it => [
    #set text(size: 32pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 2): it => [
    #set text(size: 28pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 3): it => [
    #set text(size: 24pt, fill: theme.primary, weight: "bold")
    #it
  ]
  set text(
    size: 20pt,
    font: "Manrope",
    weight: "light",
  )
  [
    = #title
    #v(24pt)
    #grid(
      columns: (1fr, 1fr),
      gutter: 0.5in,
      contentLeft,
      contentRight,
    )
  ]
}

#let layoutDTwoCols(
  contentLeft: [],
  contentRight: [],
) = {
  set page(
    width: 13.3333in,
    height: 7.5in,
    background: image("./slide-layouts/twoV1.svg"),
    margin: (top: 0.5in, bottom: 1in, left: 1in, right: 1in),
  )
  show heading.where(level: 1): it => [
    #set text(size: 32pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 2): it => [
    #set text(size: 28pt, fill: theme.primary, weight: "bold")
    #it
  ]
  show heading.where(level: 3): it => [
    #set text(size: 24pt, fill: theme.primary, weight: "bold")
    #it
  ]
  set text(
    size: 20pt,
    font: "Manrope",
    weight: "light",
  )
  [
    #grid(
      columns: (1fr, 2.3fr),
      gutter: 0.6in,
      contentLeft,
      contentRight,
    )
  ]
}

#let mainTitle(
  title: lorem(8),
  subtitle: lorem(5),
  content: [],
) = {
  layoutBTwoCols(
    contentLeft: [
      #v(1.5fr)
      = #title

      #text(
        size: 20pt,
        weight: "semibold",
        subtitle,
      )
      #v(0.4fr)
    ],
    contentRight: [
      #content
    ],
  )
}
