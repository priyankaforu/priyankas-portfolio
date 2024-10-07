title: Zero-Player Game
date: 2024-10-07
genre: Math & Computing
-----------------------

We all are players, playing different roles in different games of our lives. But what do you say? If I call this a simulation like we see in those Sci-fi movies. Everything is automated and we are trying to figure out the rules to make or break the automation processes as we watched in the movie “The Matrix”. 

In the 1940s, John Von Neumann was working on self-replicating systems and the core idea was “A robot building another robot”. While working on this project, Neumann gave birth to the “Cellular automaton” a system of building systems, a self-replicator model. Think of this model as RNA molecules in our body that contain all the information to make the exact copy of one’s self. How simple it seems right? but not, building this machine that produces other machines is typically complicated and involves a lot of computing. Despite all the complexities that include producing machines along with their copies, Von Neumann came up with a model in which each square (or a cell) has 29 states that produce the copies of itself.

The concept of this Cellular Automaton became famous when the Mathematician, Martin Gardener published an article in the Mathematical Games column of Scientific American Magazine (Refer to Issue:<a href="https://www.scientificamerican.com/issue/sa/1970/10-01/" target="_blank"> 1970, October 10th</a>). Conway, a Mathematician who has several noticeable works in  Mathematics came up with his amazing work of making the cell unpredictable. Though the inspiration is from Jon Von Neumann’s model, unlike Von Neumann’s 29 states of the cell, Conway’s model has only one square with the two states. The square should be either alive or dead. The dead cells can become alive and vice versa. The rules are very simple, yet the outcomes are completely unpredictable.

<p style="display: flex; justify-content: center; align-items: center; gap: 20px;margin-top: 30px; margin-bottom: 30px">
<img src="/static/images/image1.png" alt="A green colored cell, represing the living cell" width="30%">
<img src="/static/images/image2.png" alt="The 8 cells that surrounding the green cell are neighbors" width="30%">
</p>

The alive state is highlighted here in the above figure as “Green” and any other cell that is not highlighted is a dead cell. Every cell has 8 neighbours, For instance, observe that green cell in the image. All the red cells are neighbours of the green cell.

#### The Rules Of The Game.

1. Any living cell with less than 2 neighbours will die, because of the underpopulation.
2. Any living cell with more than 3 neighbours will die due to overpopulation.
3. Any dead cell with exactly 3 living neighbours will come to life and turn into a living cell. You see..! This is the concept of reproduction.

The important thing to note here is the grid follows the <a href="https://en.wikipedia.org/wiki/Toroidal_coordinates" target="_blank">Toroidal approach </a> which is nothing but the wrapped grid. That means if you take any edges or corners of the grid, the neighbours lie on all the opposite ends of the grid. For example, consider the grid in the figure below. The neighbours of <span style ="font-style: italic;">(0,0) are {(0,1),(1,0),(1,1)}, {(0,7),(7,1)} and the bottom right corner one (7,8)</span>. Just like wrapping it to the ends of the grid <span style="font-style: italic; opacity: 0.4;">(Marked as '*')</span>

<figure style="margin: 0 auto; width: 40%; text-align: center;">
  <img src="/static/images/image3.png" alt="The 7*8 grid" style="width: 100%; display: block;">
  <figcaption style="margin-bottom: 16px;font-weight: 300; opacity: 0.7;font-style: italic;">(The 7*8 grid)</figcaption>
</figure>

Let us simulate by inputting random cells, observe the four sequential grids <span style="font-style: italic; opacity: 0.8;">(figure 1 to 4)</span> to understand and analyse the process of automaton. At some point all the cells can be dead or the cell can form the symmetry and once the symmetry  is reached it can never be gone. Look at these <a href="https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Examples_of_patterns" target="_blank"> structures </a>for a detailed understanding.

<figure style="margin: 0 auto; width: 100%; text-align: center;">
  <img src="/static/images/image4.png" alt="The 7*8 grid" style="padding-top: 16px;width: 100%; display: block;">
  <figcaption style="margin-bottom: 16px;font-weight: 300; opacity: 0.7;font-style: italic;">(The sequence of automaton)</figcaption>
</figure>

I am no expert in delving deeper into this, but I am always fascinated how nature is built by the maths. If we look deeper in to physics, we can discover the new domain called chemistry and if we look deeper into chemistry we can something and that is the pure math, just math and this is the secret language of universe. Out of the curiosity and just for sake of fun I tried writing the program to execute this “Conways game” and I entirely credit my teacher Al Sweigart <span style="font-style: italic; opacity: 0.5;"> (Though he is not physically teaching me, I am learning through his knowledge ocean  <a href="https://alsweigart.com/" target="_blank" style="color: black;">available online)</a></span>. I wonder how he simplified the explanation and code for such complex concept. Visit this <a href="https://inventwithpython.com/bigbookpython/project13.html" target="_blank">blog to understand and program </a> it,in python. If you understand the concept of "List" in python you are good to go for programming this. The best way to learn math is programming, where you can understand the fundamental blocks like building logics and alanyse the complex parts which you thought that you never would understand so easily.
