/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */
import {
  waitForEvent
} from "../../chunks/chunk.F25QOBDY.js";
import {
  prefersReducedMotion
} from "../../chunks/chunk.L6CIKOFQ.js";
import "../../chunks/chunk.JHZRD2LV.js";

// src/components/carousel/scroll-controller.ts
var ScrollController = class {
  constructor(host) {
    this.dragging = false;
    this.scrolling = false;
    this.mouseDragging = false;
    this.handleScroll = () => {
      if (!this.scrolling) {
        this.scrolling = true;
        this.host.requestUpdate();
      }
    };
    this.handleScrollEnd = () => {
      if (this.scrolling && !this.dragging) {
        this.scrolling = false;
        this.host.requestUpdate();
      }
    };
    this.handlePointerDown = (event) => {
      if (event.pointerType === "touch") {
        return;
      }
      const canDrag = this.mouseDragging && event.button === 0;
      if (canDrag) {
        event.preventDefault();
        this.host.scrollContainer.addEventListener("pointermove", this.handlePointerMove);
      }
    };
    this.handlePointerMove = (event) => {
      const scrollContainer = this.host.scrollContainer;
      const hasMoved = !!event.movementX || !!event.movementY;
      if (!this.dragging && hasMoved) {
        scrollContainer.setPointerCapture(event.pointerId);
        this.handleDragStart();
      } else if (scrollContainer.hasPointerCapture(event.pointerId)) {
        this.handleDrag(event);
      }
    };
    this.handlePointerUp = (event) => {
      this.host.scrollContainer.releasePointerCapture(event.pointerId);
      this.handleDragEnd();
    };
    this.host = host;
    host.addController(this);
  }
  async hostConnected() {
    const host = this.host;
    await host.updateComplete;
    const scrollContainer = host.scrollContainer;
    scrollContainer.addEventListener("scroll", this.handleScroll, { passive: true });
    scrollContainer.addEventListener("scrollend", this.handleScrollEnd, true);
    scrollContainer.addEventListener("pointerdown", this.handlePointerDown);
    scrollContainer.addEventListener("pointerup", this.handlePointerUp);
    scrollContainer.addEventListener("pointercancel", this.handlePointerUp);
  }
  hostDisconnected() {
    const host = this.host;
    const scrollContainer = host.scrollContainer;
    scrollContainer.removeEventListener("scroll", this.handleScroll);
    scrollContainer.removeEventListener("scrollend", this.handleScrollEnd, true);
    scrollContainer.removeEventListener("pointerdown", this.handlePointerDown);
    scrollContainer.removeEventListener("pointerup", this.handlePointerUp);
    scrollContainer.removeEventListener("pointercancel", this.handlePointerUp);
  }
  handleDragStart() {
    const host = this.host;
    this.dragging = true;
    host.scrollContainer.style.setProperty("scroll-snap-type", "unset");
    host.requestUpdate();
  }
  handleDrag(event) {
    this.host.scrollContainer.scrollBy({
      left: -event.movementX,
      top: -event.movementY
    });
  }
  handleDragEnd() {
    const host = this.host;
    const scrollContainer = host.scrollContainer;
    scrollContainer.removeEventListener("pointermove", this.handlePointerMove);
    const startLeft = scrollContainer.scrollLeft;
    const startTop = scrollContainer.scrollTop;
    scrollContainer.style.removeProperty("scroll-snap-type");
    const finalLeft = scrollContainer.scrollLeft;
    const finalTop = scrollContainer.scrollTop;
    scrollContainer.style.setProperty("scroll-snap-type", "unset");
    scrollContainer.scrollTo({ left: startLeft, top: startTop, behavior: "auto" });
    scrollContainer.scrollTo({ left: finalLeft, top: finalTop, behavior: prefersReducedMotion() ? "auto" : "smooth" });
    requestAnimationFrame(async () => {
      if (startLeft !== finalLeft || startTop !== finalTop) {
        await waitForEvent(scrollContainer, "scrollend");
      }
      scrollContainer.style.removeProperty("scroll-snap-type");
      this.dragging = false;
      host.requestUpdate();
    });
  }
};
export {
  ScrollController
};
