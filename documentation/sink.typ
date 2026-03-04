#import "common/lib/contentBox.typ": contentBox
#import "common/lib/slideLayouts.typ": theme, mainTitle, layoutA, layoutATwoCols, layoutATwoColsWithTitle, layoutBTwoCols, layoutC, layoutCTwoColsWithTitle, layoutDTwoCols

#mainTitle(
  title: "A slide layout ideal for section titles",
  subtitle: "With a slot for a subtitle",
)

#mainTitle(
  title: "A slide layout ideal for section titles",
  subtitle: "With a slot for a subtitle",
  content: [
    #text(
      fill: white,
      size: 20pt,
      [
        #lorem(20)
      ],
    )
  ]
)

#mainTitle(
  title: "A slide layout ideal for section titles",
  subtitle: "With a slot for a subtitle",
  content: [
    #v(140pt)
    #contentBox(
      fill: theme.primaryLightest,
      text(
        fill: white,
        size: 20pt,
        [
          #lorem(20)
        ],
      ),
    )
  ],
)

#mainTitle(
  title: "A slide layout ideal for section titles",
  subtitle: "With a slot for a subtitle",
  content: [
    #v(140pt)
    #contentBox(
      fill: luma(150, 30%),
      text(
        fill: white,
        size: 20pt,
        [
          #lorem(20)
        ],
      ),
    )
  ],
)

#layoutA(
  content: [
    = Single column heading 1st
    #lorem(20)
    == Single column heading 2nd
    #lorem(20)
    === Single column heading 3rd
    #lorem(20)
  ]
)

#layoutATwoCols(
  contentLeft: [
    == Column left
    #lorem(20)
  ],
  contentRight: [
    == Column right
    #lorem(20)
  ],
)

#layoutATwoColsWithTitle(
  title: "Title in the center with two columns",
  contentLeft: [
    #lorem(20)
  ],
  contentRight: [
    #lorem(20)
  ],
)

#layoutBTwoCols(
  contentLeft: [
    = Title in the left
    #lorem(20)
  ],
  contentRight: [
    #text(
      fill: white,
      [
        #lorem(20)
      ],
    )
  ],
)

#layoutC(
  title: "Title aligned at the top",
  content: [
    #lorem(20)
    == Single column heading 2nd
    #lorem(20)
    === Single column heading 3rd
    #lorem(20)
  ]
)

#layoutCTwoColsWithTitle(
  title: "Title aligned at the top",
  contentLeft: [
    == Column left
    #lorem(20)
  ],
  contentRight: [
    == Column right
    #lorem(20)
  ],
)

#layoutDTwoCols(
  contentLeft: [
    #v(140pt)
    #text(
      fill: white,
      size: 20pt,
      [
        #lorem(20)
      ],
    )
  ],
  contentRight: [
    #v(80pt)
    = Title in the right
    #lorem(20)
  ],
)
