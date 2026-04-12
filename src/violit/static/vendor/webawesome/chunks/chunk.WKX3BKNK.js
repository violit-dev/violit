/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/components/page/page.mobile.styles.ts
var page_mobile_styles_default = (breakpoint = "768px") => `
  @media screen and (width < ${breakpoint}) {
    [part~='navigation'] {
      display: none;
    }

    :host(:not([disable-navigation-toggle])) slot[name~='navigation-toggle'] {
      display: contents;
    }
  }
`;

export {
  page_mobile_styles_default
};
