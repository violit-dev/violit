/*! Copyright 2026 Fonticons, Inc. - https://webawesome.com/license */

// src/internal/drag.ts
function drag(container, options) {
  function move(pointerEvent) {
    const dims = container.getBoundingClientRect();
    const defaultView = container.ownerDocument.defaultView;
    const offsetX = dims.left + defaultView.pageXOffset;
    const offsetY = dims.top + defaultView.pageYOffset;
    const x = pointerEvent.pageX - offsetX;
    const y = pointerEvent.pageY - offsetY;
    if (options?.onMove) {
      options.onMove(x, y);
    }
  }
  function stop() {
    document.removeEventListener("pointermove", move);
    document.removeEventListener("pointerup", stop);
    if (options?.onStop) {
      options.onStop();
    }
  }
  document.addEventListener("pointermove", move, { passive: true });
  document.addEventListener("pointerup", stop);
  if (options?.initialEvent instanceof PointerEvent) {
    move(options.initialEvent);
  }
}
var supportsTouch = typeof window !== "undefined" && "ontouchstart" in window;
var DraggableElement = class {
  constructor(el, options) {
    this.isActive = false;
    this.isDragging = false;
    this.handleDragStart = (event) => {
      const clientX = "touches" in event ? event.touches[0].clientX : event.clientX;
      const clientY = "touches" in event ? event.touches[0].clientY : event.clientY;
      if (this.isDragging || // Prevent right-clicks from triggering drags
      !supportsTouch && event.buttons > 1) {
        return;
      }
      this.isDragging = true;
      document.addEventListener("pointerup", this.handleDragStop);
      document.addEventListener("pointermove", this.handleDragMove);
      document.addEventListener("pointercancel", this.handleDragStop);
      document.addEventListener("touchend", this.handleDragStop);
      document.addEventListener("touchmove", this.handleDragMove);
      document.addEventListener("touchcancel", this.handleDragStop);
      this.options.start(clientX, clientY);
    };
    this.handleDragStop = (event) => {
      const clientX = "changedTouches" in event ? event.changedTouches[0].clientX : event.clientX;
      const clientY = "changedTouches" in event ? event.changedTouches[0].clientY : event.clientY;
      this.isDragging = false;
      document.removeEventListener("pointerup", this.handleDragStop);
      document.removeEventListener("pointermove", this.handleDragMove);
      document.removeEventListener("pointercancel", this.handleDragStop);
      document.removeEventListener("touchend", this.handleDragStop);
      document.removeEventListener("touchmove", this.handleDragMove);
      document.removeEventListener("touchcancel", this.handleDragStop);
      this.options.stop(clientX, clientY);
    };
    this.handleDragMove = (event) => {
      const clientX = "touches" in event ? event.touches[0].clientX : event.clientX;
      const clientY = "touches" in event ? event.touches[0].clientY : event.clientY;
      window.getSelection()?.removeAllRanges();
      this.options.move(clientX, clientY);
    };
    this.element = el;
    this.options = {
      start: () => void 0,
      stop: () => void 0,
      move: () => void 0,
      ...options
    };
    this.start();
  }
  /** Start listening to drags. */
  start() {
    if (!this.isActive) {
      this.element.addEventListener("pointerdown", this.handleDragStart);
      if (supportsTouch) {
        this.element.addEventListener("touchstart", this.handleDragStart);
      }
      this.isActive = true;
    }
  }
  /** Stop listening to drags. */
  stop() {
    document.removeEventListener("pointerup", this.handleDragStop);
    document.removeEventListener("pointermove", this.handleDragMove);
    document.removeEventListener("pointercancel", this.handleDragStop);
    document.removeEventListener("touchend", this.handleDragStop);
    document.removeEventListener("touchmove", this.handleDragMove);
    document.removeEventListener("touchcancel", this.handleDragStop);
    this.element.removeEventListener("pointerdown", this.handleDragStart);
    if (supportsTouch) {
      this.element.removeEventListener("touchstart", this.handleDragStart);
    }
    this.isActive = false;
    this.isDragging = false;
  }
  /** Starts or stops the drag listeners. */
  toggle(isActive) {
    const isGoingToBeActive = isActive !== void 0 ? isActive : !this.isActive;
    if (isGoingToBeActive) {
      this.start();
    } else {
      this.stop();
    }
  }
};

export {
  drag,
  DraggableElement
};
