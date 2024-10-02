<script lang="ts">
	import { browser } from '$app/environment';
	import { apiEndpoint, promptDefault, promptTemplate } from '$lib/config';
	import pkg from 'lodash';
	import { RefreshCwIcon, Trash2Icon, ThumbsUpIcon, ThumbsDownIcon } from 'lucide-svelte';
	import { marked } from 'marked';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';

	const { shuffle } = pkg;

	export let data: PageData;

	let element: HTMLElement;

	let exampleQuestions: string[] = shuffle(data.questions).slice(0, 3);
	let showExampleQuestions = true;

	$: {
		if (Object.keys(chatHistory).length > 0) {
			exampleQuestions = shuffle(data.questions).slice(0, 3);
		}
	}

	let query: string = '';

	let chatHistory: {
		[timestamp: number]: {
			question: string;
			isRetry: boolean;
			answer: {
				source_nodes?: never[];
				response: string;
			};
			spanId: string;
			feedback?: boolean;
		};
	} = browser && JSON.parse(localStorage.getItem('chatHistory') || '{}');
	let isBusy = false;

	let showHelp = false;

	async function toggleHelp() {
		showHelp = !showHelp;
	}

	let prompt: string = (browser && localStorage.getItem('prompt')) || '';
	let newPrompt: string = prompt;
	let showCustomisePrompt = false;

	async function toggleExampleQuestions() {
		showExampleQuestions = !showExampleQuestions;
	}

	async function handleSubmit(retry: boolean = false) {
		if (!query) {
			return;
		}

		scrollToBottom();

		isBusy = true;

		const timestamp = Date.now();
		chatHistory[timestamp] = {
			question: query,
			isRetry: retry,
			answer: {
				response: ''
			},
			spanId: ''
		};

		const body: { q: string; prompt?: string } = { q: query };
		if (prompt) {
			body.prompt = prompt;
		}

		query = '';

		const response = await fetch(`${apiEndpoint}/query`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(body)
		});

		if (response.ok) {
			const json = await response.json();
			chatHistory[timestamp].answer = json.response;
			chatHistory[timestamp].spanId = json.span_id;
		} else {
			console.error('Failed to get an answer:', response);
			chatHistory[timestamp].answer = { response: 'Error: Failed to get an answer' };
		}

		localStorage.setItem('chatHistory', JSON.stringify(chatHistory));

		isBusy = false;

		scrollToBottom();
	}

	async function scrollToBottom() {
		if (element) {
			setTimeout(() => {
				element.scrollIntoView({ behavior: 'smooth', block: 'end' });
			}, 100);
		}
	}

	async function handleExampleQuestion(question: string) {
		query = question;
		handleSubmit();
	}

	async function handleRetryQuestion(question: string) {
		query = question;
		handleSubmit(true);
	}

	async function deleteChat(timestamp: number) {
		delete chatHistory[timestamp];
		// trigger reactivity
		chatHistory = chatHistory;
		localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
	}

	function getSchoolUrl(file: string) {
		return `../schools/${file.replace('.json', '')}`;
	}

	async function clearChatHistory() {
		chatHistory = {};
		localStorage.removeItem('chatHistory');
	}

	async function saveBotPrompt() {
		showCustomisePrompt = false;

		prompt = newPrompt.trim();
		localStorage.setItem('prompt', prompt);

		if (prompt) {
			prompt = `${prompt}\n${promptTemplate}`;
		}
	}

	async function handleFeedback(timestamp: number, spanId: string, isPositive: boolean) {
		chatHistory[timestamp].feedback = isPositive;
		chatHistory = chatHistory;

		localStorage.setItem('chatHistory', JSON.stringify(chatHistory));

		try {
			const response = await fetch(`${apiEndpoint}/feedback`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ span_id: spanId, is_positive: isPositive })
			});

			if (!response.ok) {
				console.error('Failed to submit feedback:', response);
			}
		} catch (error) {
			console.error('Error submitting feedback:', error);
		}
	}

	let showFeedbackStats = false;

	async function toggleFeedbackStats() {
		showFeedbackStats = !showFeedbackStats;
		if (showFeedbackStats) {
			await fetchFeedbackStats();
		}
	}

	let feedbackStats = {
		total_queries: 0,
		queries_without_feedback: 0,
		positive_feedback: 0,
		negative_feedback: 0
	};

	async function fetchFeedbackStats() {
		try {
			const response = await fetch(`${apiEndpoint}/feedback`);
			if (response.ok) {
				feedbackStats = await response.json();
			} else {
				console.error('Failed to fetch feedback stats:', response);
			}
		} catch (error) {
			console.error('Error fetching feedback stats:', error);
		}
	}

	onMount(() => {
		scrollToBottom();
	});
</script>

<section>
	<hgroup>
		<h1>Interactive school records <em>chatbot</em></h1>
		<p>
			Explore the school records through an AI-powered question-answering system. Ask about schools,
			events, or any aspect of the records information. To get started click on one of the example
			questions below or enter your own into the text box.
		</p>
	</hgroup>
</section>

{#if Object.keys(chatHistory).length > 0}
	<section class="chat-history">
		{#each Object.entries(chatHistory) as [timestamp, chat]}
			<article>
				<header>
					<h2>{chat.question}</h2>
					<div class="meta">
						<datetime datetime={new Date(parseInt(timestamp)).toISOString()}
							>{new Date(parseInt(timestamp)).toLocaleString()}</datetime
						>
						{#if chat.isRetry}<mark>Retried question</mark>{/if}
					</div>
				</header>
				{#if chat.answer && chat.answer.response}
					<section class="answer">{@html marked.parse(chat.answer.response)}</section>
					<hr />
					<details>
						<summary>Context used to generate this answer</summary>
						{#each chat.answer.source_nodes || [] as node}
							<blockquote>
								{@html marked.parse(node.node.text)}
								<footer>
									<cite
										>—
										<a href={getSchoolUrl(node.node.metadata.file)}>{node.node.metadata.school}</a>
									</cite>
								</footer>
							</blockquote>
						{/each}
					</details>
					<footer>
						<div class="feedback-buttons">
							<span class="visually-hidden">Was this answer helpful?</span>
							<button
								class="feedback positive outline"
								class:secondary={chat.feedback === false}
								class:filled={chat.feedback === true}
								data-tooltip="This answer was helpful"
								on:click={() => handleFeedback(parseInt(timestamp), chat.spanId, true)}
								><ThumbsUpIcon /></button
							>
							<button
								class="feedback negative outline"
								class:secondary={chat.feedback === true}
								class:filled={chat.feedback === false}
								data-tooltip="This answer was not helpful"
								on:click={() => handleFeedback(parseInt(timestamp), chat.spanId, false)}
								><ThumbsDownIcon /></button
							>
						</div>
						<div class="action-buttons">
							<button
								class="ask-again outline"
								data-tooltip="Ask again"
								on:click={() => handleRetryQuestion(chat.question)}><RefreshCwIcon /> Retry</button
							>
							<button
								class="delete-chat outline"
								data-tooltip="Delete this entry"
								on:click={() => deleteChat(parseInt(timestamp))}><Trash2Icon /> Delete</button
							>
						</div>
					</footer>
				{:else if isBusy}
					<progress />
				{/if}
			</article>
		{/each}
	</section>
{/if}

{#if showExampleQuestions}
	<section class="example-questions">
		<hgroup>
			<h2>Example questions</h2>
			<p>
				AI-generated questions, created during data processing, to help explore the school records.
				These change randomly and may occasionally be imperfect.
			</p>
		</hgroup>
		<section class="grid">
			{#each exampleQuestions as question}
				<article>
					{#if question.length > 120}
						<span>
							{question.slice(0, 120)}...
							<!-- svelte-ignore a11y-invalid-attribute -->
							<a href="#" on:click|preventDefault={() => alert(question)}>Show more</a>
						</span>
					{:else}
						{question}
					{/if}
					<footer>
						<button
							class="outline"
							on:click={() => handleExampleQuestion(question)}
							disabled={isBusy}>Ask</button
						>
					</footer>
				</article>
			{/each}
		</section>
	</section>
{/if}

<section bind:this={element}>
	<form on:submit|preventDefault={() => handleSubmit()}>
		<!-- svelte-ignore a11y-no-redundant-roles -->
		<fieldset role="group">
			<input
				bind:value={query}
				disabled={isBusy}
				placeholder="Ask a question about the school records..."
			/>
			<button type="submit" disabled={isBusy || !query}>Ask</button>
		</fieldset>
	</form>
	<section class="grid">
		<button class="secondary" on:click={toggleHelp}>Help</button>
		<button class="secondary" on:click={toggleExampleQuestions}>
			{showExampleQuestions ? 'Hide' : 'Show'} examples
		</button>
		<button class="secondary" on:click={() => (showCustomisePrompt = true)}
			>Customise the bot</button
		>
		<button class="secondary" on:click={toggleFeedbackStats}>
			{showFeedbackStats ? 'Hide' : 'Show'} feedback stats
		</button>
		<button class="secondary" on:click={clearChatHistory}>Clear the chat</button>
	</section>
</section>

{#if showHelp}
	<dialog open>
		<article>
			<header>
				<button aria-label="Close" rel="prev" on:click={toggleHelp}></button>
				<h3>How to use the school records chatbot</h3>
			</header>
			<section>
				<h4>Getting started</h4>
				<p>
					Welcome to the interactive school records chatbot! This AI system (RAG) allows you to
					explore and inquire about the Aboriginal school records.
				</p>

				<h4>What is RAG?</h4>
				<p>
					This chatbot uses a technique called Retrieval-Augmented Generation (RAG). RAG combines
					the power of large language models with a knowledge base of specific information:
				</p>
				<ul>
					<li>
						When you ask a question, the system first retrieves relevant information from its
						database of school records.
					</li>
					<li>
						It then uses this retrieved information to generate a response, ensuring answers are
						grounded in the actual historical data.
					</li>
					<li>
						This approach helps provide more accurate and contextually relevant answers about the
						Aboriginal school records.
					</li>
				</ul>

				<h4>Asking questions</h4>
				<ul>
					<li>
						Type your question in the input box at the bottom of the page and click "Ask" or press
						Enter.
					</li>
					<li>You can ask about schools, events, or any aspect of the records information.</li>
					<li>Be specific in your questions for more accurate answers.</li>
				</ul>

				<h4>Example questions</h4>
				<p>
					Not sure what to ask? Click the "Show examples" (open by default) button to see some
					sample questions. Click "Ask" next to any example to use it.
				</p>

				<h4>Chat history</h4>
				<ul>
					<li>Your conversation history is displayed above the input box.</li>
					<li>Each entry shows your question, the AI's response, and the sources used.</li>
					<li>Use the "Retry" button (refresh icon) to ask the same question again.</li>
					<li>Use the "Delete" button (trash icon) to delete individual chat entries.</li>
				</ul>

				<h4>Customising the bot</h4>
				<p>
					Click "Customise the bot" to modify how the AI responds. You can specify the AI's role and
					give it special instructions. You can also view the default prompt used by the AI by
					expanding the "Default prompt" section.
				</p>

				<h4>Providing feedback</h4>
				<p>After each answer, you can provide feedback to help improve the chatbot:</p>
				<ul>
					<li>Click the thumbs-up icon if the answer was helpful and accurate.</li>
					<li>Click the thumbs-down icon if the answer was not helpful or contained errors.</li>
					<li>Your feedback can help improve the quality of responses for future queries.</li>
				</ul>

				<h4>Additional features</h4>
				<ul>
					<li>Clear the entire chat history using the "Clear the chat" button.</li>
					<li>
						View the context used for each answer by expanding the "Context used to generate this
						answer" section.
					</li>
				</ul>

				<h4>Tips for best results</h4>
				<ul>
					<li>Ask one question at a time for clearer answers.</li>
					<li>If you don't get the information you need, try rephrasing your question.</li>
					<li>
						Use the "Retry" feature if you think the AI missed something in its first response.
					</li>
				</ul>
			</section>
			<footer>
				<button class="secondary" on:click={toggleHelp}>Close</button>
			</footer>
		</article>
	</dialog>
{/if}

{#if showCustomisePrompt}
	<dialog open>
		<article>
			<header>
				<button aria-label="Close" rel="prev" on:click={() => (showCustomisePrompt = false)}
				></button>
				<h3>Customise the bot</h3>
			</header>
			<textarea
				bind:value={newPrompt}
				placeholder="Specify the AI's role, how to use context and query, and any specific instructions on how the bot should respond."
				rows="10"
				cols="80"
			></textarea>
			<details>
				<summary>Default prompt</summary>
				<div>{@html marked.parse(promptDefault)}</div>
			</details>
			<footer>
				<button class="secondary" on:click={() => (showCustomisePrompt = false)}>Cancel</button>
				<button on:click={saveBotPrompt}>Save</button>
			</footer>
		</article>
	</dialog>
{/if}

{#if showFeedbackStats}
	<dialog open>
		<article>
			<header>
				<button aria-label="Close" rel="prev" on:click={toggleFeedbackStats}></button>
				<h3>Feedback statistics</h3>
			</header>
			<section>
				<table>
					<thead>
						<tr>
							<th>Metric</th>
							<th>Count</th>
							<th>Percentage</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>Total queries</td>
							<td>{feedbackStats.total_queries}</td>
							<td>100%</td>
						</tr>
						<tr>
							<td>Queries without feedback</td>
							<td>{feedbackStats.queries_without_feedback}</td>
							<td>
								{(
									(feedbackStats.queries_without_feedback / feedbackStats.total_queries) *
									100
								).toFixed(2)}%
							</td>
						</tr>
						<tr>
							<td>Positive feedback</td>
							<td>{feedbackStats.positive_feedback}</td>
							<td>
								{((feedbackStats.positive_feedback / feedbackStats.total_queries) * 100).toFixed(
									2
								)}%
							</td>
						</tr>
						<tr>
							<td>Negative feedback</td>
							<td>{feedbackStats.negative_feedback}</td>
							<td>
								{((feedbackStats.negative_feedback / feedbackStats.total_queries) * 100).toFixed(
									2
								)}%
							</td>
						</tr>
					</tbody>
				</table>
			</section>
			<footer>
				<button class="secondary" on:click={toggleFeedbackStats}>Close</button>
			</footer>
		</article>
	</dialog>
{/if}

<style>
	.example-questions {
		margin-top: 2rem;
	}
	.example-questions article {
		align-items: center;
		border-radius: var(--pico-border-radius);
		box-shadow: var(--pico-box-shadow);
		display: flex;
		flex-direction: column;
		margin-bottom: 1rem;
		padding: 1rem;
		text-align: center;
	}

	.example-questions article footer {
		background-color: inherit;
		border: none;
		margin-top: auto;
		width: 100%;
		display: flex;
		justify-content: space-around;
		padding-top: 1rem;

		& button {
			font-size: 0.8rem;
			min-width: auto;
			padding: 0.3rem 0.5rem;
		}
	}

	.chat-history article footer {
		display: flex;
		font-size: 0.8rem;
		gap: 0.5rem;
		justify-content: space-between;
		text-align: right;

		& button {
			font-size: 0.8rem;
			min-width: auto;
			padding: 0.3rem 0.5rem;

			& svg {
				width: 0.8rem;
			}
		}
	}

	div.meta {
		display: flex;
		justify-content: space-between;
	}

	.answer {
		border-left: 5px solid var(--pico-primary);
		padding-left: 0.5rem;
	}

	details summary {
		font-weight: bold;
	}

	.feedback-buttons button {
		border: none;
		padding: 0.5rem 0.2rem !important;
	}

	.feedback.filled {
		& svg {
			stroke-width: 3px;
		}
	}

	.visually-hidden {
		display: none;
	}
</style>
