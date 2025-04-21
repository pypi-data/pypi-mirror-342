# Overview

# `Audio2Topics` Package 🔊🗂️

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Total downloads](https://static.pepy.tech/badge/audio2topics)](https://pepy.tech/projects/audio2topics?timeRange=threeMonths&category=version&includeCIDownloads=true&granularity=daily&viewType=chart&versions)

<img src="https://www.dropbox.com/scl/fi/3ob74o055v4df2zv6cvpe/GUI.svg?rlkey=e6k8ncw0aifz7lixnncyhkazn&st=zj16kdla&raw=1" width="500" alt="GUI Screenshot">

`Audio2Topics` is python packge that automizes topic extraction from voice and text files. The package is originally designed to aid researchers that performs interview research. Interview research typically incorporates a series of steps, starting from planning research questions, performing interviews, transcribing, and thorough manual text analysis to extract the main themes and topics of the transcribed text. This manual analysis phase is usually long and time-consuming. Additionally, the feasibility of manual analysis is limited by the volume of transcribed data.  `Audio2Topics` accelerating this step by automtically converting voice files of interviews into topics simply and effectively.

The application provides an end-to-end pipeline that handles:

- Audio transcription using OpenAI's Whisper
- Text preprocessing and cleaning
- Topic modeling with multiple algorithms
- Topic validation and optimization
- Advanced visualizations
- Model comparison and evaluation

Audio2Topics bridges the gap between audio content and text analysis, making topic discovery accessible to researchers, content creators, analysts, and anyone who needs to identify key themes in audio materials.

The full documentation is here: https://mohsenaskar.github.io/python-libraries-docs/audio2topics/ 

## Key Features

- **Automated Audio Transcription**: Convert audio files to text using state-of-the-art speech recognition
- **Advanced Text Processing**: Clean and normalize text with customizable preprocessing options
- **Multiple Topic Modeling Approaches**: Choose from BERTopic, LDA, and NMF algorithms
- **Interactive Topic Exploration**: Visualize and explore topics through multiple visualization techniques
- **Topic Quality Validation**: Assess topic coherence, diversity, and coverage
- **Topic Highlighting**: See how topics appear in original text with color highlighting
- **Model Comparison**: Compare different topic modeling approaches side by side
- **LLM Integration**: Enhance topic interpretability with AI-generated descriptions
- **Comprehensive Reporting**: Generate detailed reports with findings and visualizations

## Workflow Overview

The Audio2Topics application guides users through a structured workflow:

1. **Audio Transcription** → 2. **Text Processing** → 3. **Topic Modeling** → 4. **Validation & Visualization** → 5. **Topics Comparison**

### 1. Audio Transcription

The first step involves converting audio files to text using OpenAI's Whisper model:

- Upload audio files (MP3, WAV, M4A)
- Select Whisper model size (tiny to large)
- Transcribe with automatic language detection
- Review and save transcriptions

### 2. Text Processing

The transcribed text is then prepared for topic modeling:

- Clean text by removing stopwords, special characters, etc.
- Apply stemming or lemmatization
- Process multiple documents simultaneously
- Analyze text statistics for quality assessment

### 3. Topic Modeling

The core functionality extracts topics from processed text:

- Choose from multiple algorithms (BERTopic, NMF, LDA)
- Configure parameters like number of topics and n-gram range
- Extract topics with adaptive processing for challenging data
- Refine topics with LLM-generated descriptions

### 4. Validation & Visualization

Assess topic quality and explore results:

- Validate topics with coherence and diversity metrics
- Find the optimal number of topics for your data
- Create visualizations from word clouds to interactive topic maps
- Highlight topics in original text
- Compare different topic modeling approaches
- Generate reports for sharing and documentation

### 5. Comparison Module

The comparison tool enables side-by-side evaluation of different topic modeling approaches.

- Can compare between upto 5 topic modeling runs
- Creats supporting visualizations
- Create comparsion summary report

## Installation and Setup

### System Requirements

- Python 3.10 or higher
- 4GB RAM minimum (8GB+ recommended for larger models)
- NVIDIA GPU with CUDA support (optional, for faster processing)

### Dependencies

Audio2Topics relies on several key libraries:

- PyQt5 for the user interface
- OpenAI Whisper for speech recognition
- NLTK and spaCy for text processing
- BERTopic, scikit-learn, and UMAP for topic modeling
- Matplotlib, seaborn, and wordcloud for visualizations
- OpenAI/Anthropic APIs for LLM integration (optional)

### Installation Steps

1. **Install the package**

   ```
   pip install audio2topics
   ```
2. **Configure API Keys (Optional)**

   - For LLM topic refinement, configure OpenAI or Anthropic API keys in the settings menu
3. **Launch the application**
   To start the tool, activate the Python enviroment where the tool was installed and type:

   ```
   audio2topics
   ```

in the terminal.

## Use Cases

Audio2Topics serves a wide range of applications across different domains:

### Academic Research

- Analyze interview recordings for qualitative research
- Process lecture content to identify key themes
- Extract topics from academic presentations and symposia

## Best Practices

### Audio Recording Quality

- Use clear recordings with minimal background noise
- Ensure adequate volume levels
- Use lossless formats when possible

### Document Preparation

- Split long recordings into shorter segments
- Group related content into meaningful documents
- Remove irrelevant sections before processing

### Topic Modeling Strategy

1. Start with a small subset of documents to test different approaches
2. Use the Comparison tab to identify the best method for your data
3. Validate topic quality before drawing conclusions
4. Use LLM refinement for clearer topic interpretations
5. Combine quantitative metrics with human judgment

### Reporting and Sharing

- Export visualizations in appropriate formats for your audience
- Include topic words and example documents in reports
- Provide context for topics through LLM-generated descriptions
- Use interactive formats (HTML) for detailed exploration

## References and Resources

### Underlying Technologies

- [OpenAI Whisper](https://github.com/openai/whisper)
- [BERTopic](https://github.com/MaartenGr/BERTopic)
- [spaCy](https://spacy.io/)
- [scikit-learn](https://scikit-learn.org/)
- [PyQt](https://riverbankcomputing.com/software/pyqt/)

## License

Released under the MIT License: For more details, see the `LICENSE` file.
Copyright (C) 2025 **`audio2topics`**

Developed by: Mohsen Askar <ceaser198511@gmail.com>

## Citation

If you use Audio2Topics in your research, please cite:

```bibtex
@software{audio2topics2025,
    title = {Audio2Topics: A Python package to automatically extract topics from audio or text files},
    author = {Mohsen Askar},
    e-mail = {ceaser198511@gmail.com},
    year = {2025},
    url = {https://pypi.org/project/audio2topics/}
}
```
