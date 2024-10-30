# PenHealNet: An Agent-based LLM Framework for Automated Pentesting and Optimal Remediation

## Introduction
This is the official implementation for the paper "PenHealNet: An Agent-based LLM Framework for Automated Pentesting and Optimal Remediation".

## Features
- **Automated Pentesting:** Leverages LLM to identify vulnerabilities in systems automatically.
- **Optimal Remediation:** Provides effective and efficient remediation strategies tailored to the detected vulnerabilities.
- **Scalability and Adaptability:** Potential to handle large networks and diverse systems.
- **Customizability:** Allows users to tweak various parameters to suit specific organizational needs.

## Getting Started
1. Set up the target machine Metaploitable and Metasploitable2:
    - Download Metasploitable from [here](https://sourceforge.net/projects/metasploitable/files/Metasploitable2/). Obtain its IP address using `ifconfig`.
    - Download Metasploitable2 from [here](https://sourceforge.net/projects/metasploitable/files/Metasploitable2/). Obtain its IP address using `ifconfig`.
    - Set up the virtual machines using [VirtualBox](https://www.virtualbox.org/wiki/Downloads) or [UTM](https://getutm.app/).

2. Set up the attack machine
    - Install [Kali Linux](https://www.kali.org/downloads/).
    - Set up the virtual machines using [VirtualBox](https://www.virtualbox.org/wiki/Downloads) or [UTM](https://getutm.app/).
  
3. Install with:
    - `git clone https://github.com/Jaacky-Huaang/PenHealNet.git`
    - `cd PenHealNet`
    - `pip3 install -r requirements.txt`

4. Set up OpenAI API
    - Create an account on [OpenAI](https://platform.openai.com/signup) if you don't have one.
    - Link a payment method to your OpenAI account on the [OpenAI API platform](https://platform.openai.com/docs/overview)
    - Export your API key with `export OPENAI_API_KEY='<your key here>'`

5. Put your database in the `docs` folder

5. Run:
    - `python3 src/pentest_module.py`
    -  When prompted to enter the target IP address, enter the IP address of the target machine.
    - `python3 src/remediation_module.py`


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/GreyDGL/PentestGPT.svg?style=for-the-badge
[contributors-url]: https://github.com/GreyDGL/PentestGPT/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/GreyDGL/PentestGPT.svg?style=for-the-badge
[forks-url]: https://github.com/GreyDGL/PentestGPT/network/members
[stars-shield]: https://img.shields.io/github/stars/GreyDGL/PentestGPT.svg?style=for-the-badge
[stars-url]: https://github.com/GreyDGL/PentestGPT/stargazers
[issues-shield]: https://img.shields.io/github/issues/GreyDGL/PentestGPT.svg?style=for-the-badge
[issues-url]: https://github.com/GreyDGL/PentestGPT/issues
[license-shield]: https://img.shields.io/github/license/GreyDGL/PentestGPT.svg?style=for-the-badge
[license-url]: https://github.com/GreyDGL/PentestGPT/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/gelei-deng-225a10112/
[linkedin-url2]: https://www.linkedin.com/in/vmayoral/
[discord-shield]: https://dcbadge.vercel.app/api/server/eC34CEfEkK
[discord-url]: https://discord.gg/eC34CEfEkK
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
