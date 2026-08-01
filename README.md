<span style = "display: flex; align-items: center;">
	<img src="Docs/ApricityAI Logo.png" width="180">
	<div>
		<h1 align = "center"> ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ U-LARPER ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ </h1>
		<p align="center"> <b>
			Unified Latent Architecture for Recursive
			Prediction via Embedding Refinement
		</b>
		<br>
			A theorhetical architecture for persistant latent reasoning beyond Transformers
		<br>
			By engineers at Apricity AI et al
	 	</p>
	</div>
</span>

<p align="center">
<a href = "https://">Research Paper</a>
•
<a href = "Docs/">Other Documentation</a>
•
<a href = "Comparisons/">Comparisons</a></p>

<h2 align = "center"> Why U-LARPER? </h2>
<p>
Model Large Language Models (LLMs) perform reasoning explicitly by generating long series of tokens. 
<br>
U-LARPER instead proposes that reasoning should occur inside a persistent latent representation, with language generation treated as one of the means of communication between a user and the model, not the means that the model uses to think in.
<br><br>
This changes the model from:
<br>
Input -> Token -> Token -> Token
<br><br>
To:
<br>
Input -> Latent representation -> Refinement -> Output


<h2 align = "center"> Notes </h2>
<h3> Fictionality </h3>
<p>
I'm not sure if this could get me into legal trouble, so I will say:
<br>
"Apricity AI" is purely a fictional entity, any people that worked alongside me or the company are also fictional. I, the owner of this repo, represent the only real human being, company, entity, et cetera that contributed to this project.
</p>


<h3> Research </h3>
<p>
This reposority has been made alongside and accompanies a research paper. The research paper goes into detail on:
<ul>
<li>
Motivation
</li>
<li>
Architecture
</li>
<li>
Training methodology
</li>
<li>
Multi-modality
</li>
<li>
Retrieval and memory
</li>
<li>
Possible future reserach
</li>
</ul>
</p>

<h3> Programming </h3>
NO GENERATIVE AI WAS USED TO CREATE THIS
<br>
I also did not know how to use PyTorch. Earlier commits will certainly show some "artifacts" from my learning process. Please dont be mean to me :(..


<h2 align = "center"> Overview </h2>

<p>
U-LARPER is a proposed neural architecture designed to separate reasoning from language and from generation.
Rather than repeatedly predicting the next token, U-LARPER performs a recursive iteration over a latent state before choosing when it is ready to begin decoding an output. This enabled a model using this architecture to reason independently of text generation, and allows more computation to be used when neaded depending on a problem's complexity.
Unlike traditional autoregressive models, language is treated as an interface to the reasoning process rather than the medium it is carried out in.
</p>

<h2 align = "center"> Repo Contents </h2>

```
Docs/           Some documentation covered in the research paper in mode detail
Examples/       Example implementations using files in Model/
Comparisons/    Figures and graphs comparing U-LARPER with Transformers
Model/          The U-LARPER architecture 'backend'
```