# fresh-banana
An application in response to Marina Wyss' challenge on YouTube to create an application that tells when a banana will turn rotten.

The challenge: https://youtu.be/MFSFcPsMsuE?si=N5EfW_CstQH8nFn-&t=649

If you've come across this project and would like to contribute, please feel free to reach out!

The purpose of this project is to build on my machine learning skills and practice what I already know.

Everywhere in this project, Yggdrasil is an alias for ChatGPT pair programming and research.  That's what I like to call them when I'm studying machine learning.  The name comes from Norse Mythology and refers to a sacred tree that connects Heaven and Earth.  I like to think of them as my link to the world of machine learning.

# Tentative Development Process

## Gather data

Marina pointed out that one might start with bananas of different ripeness, but I think it makes sense to just buy 50 bananas on the green side because if today, I have fifty bananas that are ten days from turning rotten, then tomorrow, I will have fifty bananas that are *nine* days from turning rotten.

I need to photograph the bananas each day, preferrably around the same time.

Extract the individual banana images from the photographs I take.

Set aside a portion of my bananas as "test" bananas to make sure I don't overfit and give myself confidence.  However, in a worst case scenario, I can gather more data by photographing more bananas.

### Progress

I purchased fifty bananas and laid them across black garbage bags in my home office, which I believe is an ideal location because it has shutters as well as an overhead light with adjustable brightness levels and color temperature levels.  With three brightness levels and three temperature levels, I get nine different images of each banana right out of the gate before turning to any kind of "data augmentation".  If my bananas were to turn brown in five days, that gives me 50 bananas x 9 lighting levels x 5 days = 2250 raw images.

2025 Aug 27 7:30 PM - first photos (I noted that glare on the black plastic background is apparent - idk if this will pose a challenge further down the line)
I also noted that my phone camera seemed to be working overtime to normalize the photos to account for different lighting conditions.  This reminds me that the equipment used to photograph the bananas can make a difference, especially if we had many users using this app, each with their own cameras.

## Data cleaning and augmentation

I imagine that I will use a paint program to turn my photographs of my bananas into smaller photographs of individual bananas.  I will search and see if there may be a tool to help with this - Definitely ask Yggdrasil to help.

Next, I will want to somehow pre-process the images to be useful for data augmentation.  At a minimum, I expect to zoom and rotate the images to make an augmented set of images.  I'm also wondering if it would make sense to put the bananas against different backgrounds - I will search and see if there may be a tool to help with this - Again, definitely ask Yggdrasil to help!

### Progress

TODO

## ML Architecture

Upon hearing Marina give the challenge, my first thought is that this sounds quite similar to MNIST digit classification.  Instead of having categories for images of handwritten digits 1, 2, 3, and so on, we could have categories for bananas with 1 day to go, 2 days to go, 3 days to go, and so on.

However, the main difference is that a handwritten 2 is logically between 1 and 3, but it doesn't logically sit between 2 and 3 on the manifold.  A banana that is 2 days from expiration should logically fall on a manifold between a 1 day banana and a 3 day banana.

Either way, it seems light a straightforward applcation for a ConvNet

For her part, Marina suggested fine-tuning an existing computer vision model.  This is something I'm not yet familiar with doing, so I'll be doing a lot of research with Google and Yggdrasil.  I'm curious about how results will compare between these two, and I'll also want to think about other possible solutions, as well.

The nice thing is that a ConvNet is something I can spin up relatively quickly given my exposure to examples of classifying MNIST digits.

### Progress

TODO

## Creating an interface

As Marina pointed out, it isn't particularly difficult to set up a web application that allows the user to upload a photo, pass the bytes of the photo to a function, and then return a response telling how many days until the banana dies.

I'm an experienced web developer by trade, and I expect this to be the easiest part.  The challenge is that I'm used to working with C#, Javascript, and .NET, and a lot of ML tools run on Python, so I'm going to have to do some research about how to make this happen.  Definitely ask Yggdrasil to help!

### Progress

TODO

## Deployment

Again, I'm familiar with the world of .NET, so I'm going to have to learn some new-to-me tools to get this up and running.

### Progress

TODO
