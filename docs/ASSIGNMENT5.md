## Assignment 5

1. Selector priority:
   1. Element selector
   2. Class selector
   3. ID selector

   This priority is derived to selectors involving children

2. Responsive design is crucial for web's versatility in cross-platform usage, although not implemented in this project D:. Almost every professional web has implemented responsive design. One of each is Chat GPT application.

3. Difference between margin, border, and padding and how to implement it
   * Margin is the reserved whitespace that exists around an object. To implement a margin, one simply needs to apply `margin: (certain-size)` in stylesheet, style tag, or style attribute, with `certain-size` unit can be in pixel, viewheight/width percentage, or absolute percentage.
   * Border is an object decoration that is located exactly in the circumference of the object. One can specify whether the border is included as the size of the object. To implement a border, one can simply add `border: (thickness/size), (style), (color)`, or `border-color: (color); border-style: (style); border: (thickness/size)` in the styling section. 
   * Padding is a whitespace that, in contrary to margin, exists within an object. To implement a padding, just simply add `padding: (certain-size)` to the styling section.

4. Flex-box and grid is a layouting format imposed to a container or any element that organizes objects within it in intuitive way, such that it eases the front-end developer. Flex-box list the objects within it vertically or horizontally, forming a one dimensional row or column, while grid allows the objects to form a table or two dimensional grid.

5. How do I do each step?
   1) For product edit and deletion functionality, I simply just defined a new routing that leads to function handler that performs necessary task, either deleting a product passed in parameter or edit sent product through form.
   2) For styling implementation, I just use raw CSS, accesible from static files
 






