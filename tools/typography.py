"""Site-wide typography tune-up, injected via the UAE header so it applies on every page.

Raleway for headings, Poppins for text; fluid heading sizes; no forced Capitalize;
comfortable line-heights; readable button text on mobile."""

CSS = r'''<style id="eh-typo">
body,.elementor-widget-text-editor,.elementor-icon-list-text,.elementor-button,.elementor-widget-button .elementor-button{font-family:Poppins,sans-serif}
body{-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}
/* UAE's hidden site title / skip link: visually hidden (their plugin CSS is missing from LiteSpeed UCSS) */
.main-title.bhf-hidden,.hfe-skip-link:not(:focus){position:absolute!important;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.elementor-heading-title{text-transform:none!important;letter-spacing:-.005em!important;text-wrap:balance}
/* page title */
h1.elementor-heading-title{font-family:Raleway,sans-serif!important;font-size:clamp(30px,3.6vw,48px)!important;line-height:1.15!important;font-weight:800!important}
/* subtitle right under the page title */
.elementor-widget-heading:has(h1)+.elementor-widget-heading .elementor-heading-title{font-size:clamp(15px,1.25vw,18px)!important;line-height:1.65!important;font-weight:400!important;max-width:760px;margin-left:auto;margin-right:auto}
/* section titles (heading followed by the decorative divider) */
.elementor-widget-heading:has(+.elementor-widget-divider) .elementor-heading-title,
.elementor-widget-heading:has(+.elementor-widget-icon-list) .elementor-heading-title{font-family:Raleway,sans-serif!important;font-size:clamp(26px,2.8vw,38px)!important;line-height:1.2!important;font-weight:800!important}
.elementor-widget-divider+.elementor-widget-text-editor{font-size:clamp(15px,1.2vw,17px)!important;line-height:1.6!important}
/* card / item titles */
.elementor-widget-heading h3.elementor-heading-title{line-height:1.3!important}
.elementor-widget-text-editor{line-height:1.7}
.elementor-widget-text-editor p{margin-bottom:.8em}
.elementor-icon-list-text{line-height:1.6!important}
@media (max-width:767px){
 .elementor-widget-heading h3.elementor-heading-title{font-size:max(15px,1em)}
 .elementor-button .elementor-button-text,.elementor-button{font-size:14px!important;line-height:1.3!important}
 .elementor-widget-text-editor{font-size:15px}
}
</style>'''
