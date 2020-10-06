# Horizon-Finding

We have calculated transition probability, emission probability and initial probability and then applied simple Bayes net to determine the mountain-ridge. Our output image shows the ridge with a blue line.

Further to improve the accuracy of determining mountain-ridge, we have implemented Viterbi algorithm and it is shown in the output image by red line.

Third approach followed by us is incorporating some human input by providing (x,y) coordinate of a single point that is sure to lie on ridgeline and it is shown by green line in the output image.


#### Output obtained by providing human_input. :-

``` python mountain.py mountain.jpg 250 147  ```

![output_simple.jpg](/sample_output/output_simple.jpg)
![output_human.jpg](/sample_output/output_human.jpg)
![output_map.jpg](/sample_output/output_map.jpg)


