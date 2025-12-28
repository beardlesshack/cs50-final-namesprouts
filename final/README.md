# namesprouts.com
#### Video Demo:
#### Description:
#### This project is a website designed to collect users name and birth-month and create a flower with the name incorporated into the stem. The main feature is to transform the letters of the name to become a continuous stem-like line that spells the name up the flowers stem.
#### Example of final piece: ![A colorful flower with the user's name written as a continuous flowing stem beneath the bloom, demonstrating the name-to-stem conversion feature][def]

[def]: render-1.png

# NameSprouts  
**CS50 Final Project – 2025**

**Project Title:** namesprouts.com  
**Project By:** Rich Fowler  
**Location:** Stuart, Florida, USA  
**Date of Video:** 12/25/25  

**GitHub Username:** beardlesshack  
**edX Username:** dbpop  

**Contact Emails:**  
- eartheus@hotmail.com  
- thenugglugg@gmail.com  

---

## Project Description

NameSprouts is a web-based application that generates personalized artwork by incorporating user-submitted names into the stems of flower designs. The application transforms textual name data into a stem-like visual structure that spells the name from the bottom upward, resembling a continuous, hand-drawn flower stem.

Each flower design corresponds to a birth month, with all twelve months represented by watercolor-style flower images. The site includes a design and edit interface, securely stores user data, and supports user authentication through a username and password system.

---

## Project Overview

The idea behind NameSprouts is to allow users to select a flower design and embed a name directly into the flower stem. Letters are arranged vertically so that the **first letter of the name appears at the bottom of the stem**, and the remaining letters stack upward to connect with the flower head.

The stem is designed to look continuous, starting with a decorative curl at the bottom and flowing upward through each letter as if drawn from a single piece of string. The primary design challenge was maintaining legibility while achieving an organic, hand-drawn appearance.

The long-term goal of the project is to support creating, editing, purchasing, and downloading printable artwork generated from user input.

---

## Unique Feature

The defining feature of NameSprouts is the transformation of a user’s name into the physical structure of a flower stem. Using cursive fonts and watercolor-style flower imagery, names are visually integrated into the design rather than placed as separate text.

Users can create multiple NameSprouts and arrange them together on a single canvas before producing a final printable composition.

---

## User Accounts and Flower Selection

Users create an account using a username and password, which are stored securely in the database.

Flower selection is based on birth months, with each month represented by a traditionally associated flower rendered in watercolor style. The selected flower image visually connects to the stem formed by the user’s name.

---

## Current State and Future Improvements

The current version of the site is fully functional for collecting user input and generating live visual previews.

Planned improvements include:
- Smoother and more continuous stem lettering  
- Improved alignment and proportional sizing of letters  
- A larger preview canvas capable of displaying multiple flowers side by side  
- Dynamic spacing based on the number of flowers and the length of names  

The final phase of development would involve purchasing the domain **namesprouts.com**, deploying the application publicly, and integrating a payment processing system.

---

## Video Demo

**<[VIDEO LINK](https://youtu.be/ctYr-tuWRWo?si=ddF3aKQQwAlgNas1)>**

---

## Technologies Used

- **Python (Flask)** for server-side logic and routing  
- **JavaScript** for live preview and DOM manipulation  
- **HTML / Jinja2** for templating  
- **CSS** for layout and visual alignment  
- **SQLite3** for database storage  

---

## Project File Overview

### `app.py`

This file contains the main Flask application and is responsible for:

- Initializing the Flask app  
- Defining application routes (login, register, design, save)  
- Handling form submissions  
- Managing user sessions  
- Connecting to the SQLite database  
- Saving and retrieving user projects  
- Registering error handlers  

**Design Choice:**  
Flask was selected because it is lightweight and aligns well with CS50’s emphasis on understanding core web application concepts without unnecessary abstraction.

---

### `templates/layout.html`

This template provides the base layout for the application. It includes:

- Overall page structure  
- Navigation bar  
- Flash message handling  
- A `{% block content %}` section extended by other templates  

Using a shared layout reduces repetition and maintains consistency across the site.

---

### `templates/design.html`

This file renders the main design interface and includes:

- Name input field  
- Birth month selection  
- Preview and save buttons  
- Flower preview image  
- Vertical container for stem letters  

Inline CSS and JavaScript are included to control preview behavior and simplify debugging.

---

### JavaScript (inline in `design.html`)

The JavaScript code handles:

- Reading user input  
- Sanitizing names to allow letters only  
- Creating one DOM element per character  
- Appending letters in natural order  
- Updating the flower image based on the selected month  
- Updating the preview dynamically without reloading the page  

**Key Design Decision:**  
Letters are appended in logical order while CSS controls the visual stacking direction. This separation keeps the data flow simple and predictable.

---

### CSS (inline in `design.html`)

CSS controls the vertical stem layout using flexbox:

```css
.stem-letters {
    display: flex;
    flex-direction: column-reverse;
}






