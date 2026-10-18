# 14. anastasis

Author: hollo

Phase 2 | webex

Flag: `labyrinth{y0u_r4is3d_th3_t4g_fr0m_th3_d34d}`.

## Description

The Labyrinth devours every forbidden mark carved into its walls. But beyond the last gate, the pieces may assemble themselves once more, and what was slain may return in another form.

## Solve

* The challenge consisted of 5 filter stages with the main goal being able to bypass them and smuggle and render an HTML tag in the note:

<img width="1420" height="922" alt="image" src="https://github.com/user-attachments/assets/0538a4d8-8dd6-43dd-a8d9-4020407740d9" />


***

Lets take a look at how the filters work individually in brief:

1. **unicode normalized**: Makes different unicode representations of the same character consistent.
2. **entity references stripped:** Removes HTML character references such as `&lt;`, `&#60;` and `&#x3c;` from the input.
3. **tags stripped:** Removes text that looks like an HTML tag. Example: `<b>`hello`</b>` → hello
4. **pybluemonday:** pybluemonday is a python library for [bluemonday](https://github.com/microcosm-cc/bluemonday) which is an HTML sanitizer. What it does is sanitize an HTML string by stripping out anything not in an allow list of tags.
5. **HTML entities decoded:** Converts any remaining HTML character references into their corresponding characters. Example: `&lt;` → `<`

The challenge had to be solved by experimenting using different payloads to understand how the filters work not just individually, but as a whole which is where the vulnerability lies. 

* for example, passing something like `&lt` (which is the HTML entity for <), gets stripped at the the entity reference filter. However, something like `& lt` with a space in between successfully survives entity stripping but doesn't get rendered because of the space. On passing something like tes`<html>`t, the tag strip filter removes the tag and produces the output as `test`.

* So based on the experiments we conducted we can theorize and form a payload that would successfully smuggle an HTML entity using the tag stripping filter to our advantage: `&<>lt`. This gets past the entity filter because of the tags in between and gets decoded from `&lt` to `<` once the tags are stripped.

***

Using this, we can now create our final payload: `&<>ltb>`

<img width="1406" height="841" alt="image" src="https://github.com/user-attachments/assets/da95460c-8988-467c-9f6d-ee818f0ba517" />



