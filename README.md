# 374learn

A PrairieLearn course for CS374: Introduction to Algorithms & Models of Computation, featuring scaffolded exercises for theoretical computer science topics.

This fork extends [TheorieLearn](https://theorielearn.github.io/) with modified and extended problems.

Public access is available at [374learn](https://374learn.d.rw). You may join the 374L class using join code WHY-P33-G4KD or going to [CSL 374](https://374learn.d.rw/pl/course_instance/1)

## Quick Setup

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- Git

### Running PrairieLearn Locally

1. **Clone this repository:**
   ```bash
   git clone https://github.com/ultraviolet/374learn.git
   cd 374learn
   ```
2. **Create job directory and start PrairieLearn:**
   ```bash
   mkdir -p ~/pl_ag_jobs
   docker run -d --name prairielearn \
     -p 80:3000 \
     -v "$PWD:/course" \
     -v ~/pl_ag_jobs:/jobs \
     prairielearn/prairielearn
   ```

3. **Access the course:**
   Open your browser to `http://your-server-ip/pl`

4. **Select your course:**
   - Click on "Load from disk"
   - Choose "TheorieLearnPublic"
   - Select the "Public" course instance
## License

**Copyright &copy; 2026 [TheorieLearn](https://theorielearn.github.io/)**

- Text: [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- Code: [MIT License](LICENSE)

## Resources

- [PrairieLearn Documentation](https://prairielearn.readthedocs.io/)
- [CS374 Course](https://courses.grainger.illinois.edu/cs374/)
- [TheorieLearn](https://theorielearn.github.io/)
