# nicegui-pdf
A NiceGUI PDF component (using pdf.js) to nicely integrate PDFs without the need for iframes without having any control on which page is shown or without the possibility to read the seelcted text. A quick example is shown below:

```python
    from nicegui import ui, app
    from nicegui_pdf.pdf_viewer import PdfViewer

    [...] 

    state = {
        "current_page": 1,
    }

    [...]

    ui.number().bind_value(state, "current_page")

    path = app.add_static_file(local_file="example/paper.pdf")
    PdfViewer(path).classes("w-full").style(
        "border: solid 1px gray;"
    ).bind_current_page(
        state
    )
```


# Features
- Full integration of PDF files into NiceGUI
- Two-way binding of `current_page`
- One-way binidng of `num_pages`, `is_rendering` and `selected_text`


A full example demonstrating all features is given in `example/main.py`:
<p align="center">
    <img src="assets/screenshot.png" alt="table" width="700"/>
</p> 



## ToDo's
- [x] Basic viewer
- [x] Text Overlay
- [x] Binding of pages etc
- [x] Binding of selected text
- [x] Support resizing
- [ ] Binding on path (load new pdf document)
- [ ] Highlight text (not 100% sure yet)
- [ ] Push to pypi


## Disclaimer
I'm neither a JS, NiceGUI or VUE expert. I simply tested a few things and found that an older version of PDF.js can be integrated as a custom NiceGUI component. Therefore, I cannot give any warranty etc. but still I'm trying to maintain this code. If you find any bugs or have feature requests, please open an issue or a pull request.

## References
- PDF.js (https://mozilla.github.io/pdf.js/)
