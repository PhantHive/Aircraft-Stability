<h1 align="center"><strong><i>AS APP</i></strong></h1>
<h3 align="center">A tool for aircraft stability calculation</h3>

<div align="center">

<img src="demo.png" alt="AS-app"/>



---


<a href="https://heroku.com/">
<img src="https://img.shields.io/badge/SCHOOL-IPSA-cyan.svg?style=for-the-badge">
</a>

<a href="https://nodejs.org/en/">
<img src="https://img.shields.io/badge/NodeJS-18.13.0-339933.svg?style=for-the-badge&logo=node.js" alt="Made with Node JS">
<img src="https://img.shields.io/badge/Express-4.18.2-000000.svg?style=for-the-badge&logo=express" alt="Made with Express">
<img src="https://img.shields.io/badge/React-18.2.0-61DAFB.svg?style=for-the-badge&logo=react" alt="Made with React">
<img src="https://img.shields.io/badge/Electron-23.1.0-47848F.svg?style=for-the-badge&logo=electron" alt="Made with Electron">
</a>

[![Issues][issues-shield]][issues-url]


</div>


### Branches

- [x] [stable] - Stable branch (complete with start.sh)

### Purpose

...

### How to run

- Clone the repository
- Install dependencies with `npm install`

### Dependencies problems
- If you have problems with dependencies, try to update using `ncu -u` and then `npm install`
- Try to delete the `package-lock.json` file and then `npm install`

### Port issues
- In case you have a port already in use you can change it a .env file in the API folder and add a **PORT** variable to change the port.
- In case you started the app and you want to change the port, you can kill the process using `npx kill-port <number of port>` and then start the app again.

### Acknowledgement



<!-- MARKDOWN LINKS & IMAGES -->
[issues-shield]: https://img.shields.io/github/issues/PhantHive/aicraft-stability.svg?style=for-the-badge&logo=github
[issues-url]: https://github.com/PhantHive/aicraft-stability/issues/