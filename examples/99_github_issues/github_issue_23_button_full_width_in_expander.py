import violit as vt


def main():
    app = vt.App()

    app.header("Button Width Issue in Expander (#23)")

    app.subheader("1. Standard Button (Should be full width)")
    app.button("Standard Button")

    with app.expander("2. Expander with Button (Issue: Button might not be full width)", expanded=True):
        app.button("Button in Expander")
        app.write("The button above should ideally take the full width of the expander, similar to the standard button.")

    app.subheader("3. Width can still be customized outside the expander")
    app.write("These buttons intentionally use custom widths to show that full width is the default, not a limitation.")
    app.button("Fixed Width Button (280px)", style="width: 280px;")
    app.button("Relative Width Button (60%)", style="width: 60%;")

    with app.expander("4. Width can also be customized inside the expander", expanded=True):
        app.write("Buttons inside the expander are full width by default now, but you can still override the width however you want.")
        app.button("Expander Fixed Width Button (280px)", style="width: 280px;")
        app.button("Expander Relative Width Button (60%)", style="width: 60%;")

    app.run()


if __name__ == "__main__":
    main()
