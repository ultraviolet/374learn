# 374learn

A PrairieLearn course for CS374: Introduction to Algorithms & Models of Computation, featuring scaffolded exercises for theoretical computer science topics.

This fork extends [TheorieLearn](https://theorielearn.github.io/) with enhanced Guided Problem Sets (GPS) for regular language transformations.

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

2. **Start PrairieLearn with Docker:**
   ```bash
   docker run -it --rm \
     -p 3000:3000 \
     -v "$PWD:/course" \
     prairielearn/prairielearn
   ```

3. **Access the course:**
   Open your browser to http://localhost:3000/pl

4. **Select your course:**
   - Click on "Load from disk"
   - Choose "TheorieLearnPublic"
   - Select the "Public" course instance

### Stopping and Restarting

To stop PrairieLearn, press `Ctrl+C` in the terminal.

To restart with a named container (recommended for persistence):
```bash
# First time
docker run -d --name prairielearn \
  -p 3000:3000 \
  -v "$PWD:/course" \
  prairielearn/prairielearn

# Restart after stopping
docker restart prairielearn

# Stop
docker stop prairielearn
```

## Course Structure

### Main Assessments

- **BANK-5: Language Transformations** - Comprehensive regular transformation exercises
  - 28 transformations with GPS format (84 questions total)
  - Each transformation includes:
    1. Introduction with concrete examples
    2. Apply transformation to a concrete DFA
    3. Symbolic NFA construction

### Key Topics

- Regular Languages & Automata (DFA/NFA)
- Regular Transformations (compress, delete, insert, reverse, etc.)
- Context-Free Languages
- Decidability & Computability
- Algorithm Design & Analysis

## Recent Updates

### GPS (Guided Problem Set) Format

All 28 regular transformation coding questions have been converted to GPS format, providing scaffolded learning from concrete examples to symbolic construction:

**Main Transformations (20):**
- compress_1, compress_2
- delete0, delete1star, delete1star_prefix, delete_fifth
- flipEvens, flipSubstring
- insert0, insert10, insert_fifth
- inv_thirds, mid, parity_runs
- proper_proper_prefix, reverse, skip
- take2skip2_1, take2skip2_2, thirds
- wRw (w^Rw), wwR (ww^R)

**Homework Transformations (8):**
- DelOnes, ThereAndBack, XOR
- Double, Move 1 Forward
- MoveBack8, Half L, Flip Substring

### Bug Fixes

- Fixed frozenset handling in automata grading (`fa_utils.py`)
- Fixed KeyError in Move 1 Forward transformation
- Corrected UUID validation issues

## Development

### File Structure

```
TheorieLearnPublic/
├── questions/
│   ├── regular_transformations/
│   │   ├── coding/              # Original coding questions
│   │   └── guided_problem_sets/  # New GPS format (84 questions)
│   └── ...
├── courseInstances/
│   └── Public/
│       └── assessments/
│           └── BANK-5/           # Language Transformations assessment
├── serverFilesCourse/
│   └── theorielearn/
│       ├── automata_utils/       # DFA/NFA utilities
│       └── regular_transformations/
└── infoCourse.json
```

### Making Changes

After modifying questions or server code:

1. Restart the PrairieLearn container:
   ```bash
   docker restart prairielearn
   ```

2. Refresh your browser (the course auto-syncs on page load)

### Testing Questions

1. Navigate to the assessment: http://localhost:3000/pl/course_instance/1/assessment_instance/5/
2. Click through each question to test functionality
3. Check for errors in:
   - Question generation (refresh if needed)
   - Answer grading
   - Visual rendering

## Contributing

This is a fork of TheorieLearn for personal CS374 practice and development. For upstream contributions, see [TheorieLearn/TheorieLearnPublic](https://github.com/TheorieLearn/TheorieLearnPublic).

## License

**Copyright &copy; 2026 [TheorieLearn](https://theorielearn.github.io/)**

- All text: [Creative Commons Attribution 4.0 (CC-BY)](https://creativecommons.org/licenses/by/4.0/)
- All code: [MIT License](LICENSE)

Based on TheorieLearn resources and [Jeff Erickson's Algorithms course materials](https://jeffe.cs.illinois.edu/teaching/algorithms/).

## Resources

- [PrairieLearn Documentation](https://prairielearn.readthedocs.io/)
- [CS374 Course Website](https://courses.grainger.illinois.edu/cs374/)
- [TheorieLearn Project](https://theorielearn.github.io/)
