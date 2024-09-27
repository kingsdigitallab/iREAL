<script lang="ts">
	import { browser } from '$app/environment';
	import { apiUrl, promptDefault, promptTemplate } from '$lib/config';
	import pkg from 'lodash';
	import { RefreshCwIcon, Trash2Icon } from 'lucide-svelte';
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
		};
	} = browser && JSON.parse(localStorage.getItem('chatHistory') || '{}');
	let isBusy = false;

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
			}
		};

		const body: { q: string; prompt?: string } = { q: query };
		if (prompt) {
			body.prompt = prompt;
		}

		query = '';

		const response = await fetch(apiUrl, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(body)
		});

		if (response.ok) {
			const answer = await response.json();
			chatHistory[timestamp].answer = answer;
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

	onMount(() => {
		scrollToBottom();
	});
</script>

<section>
	<hgroup>
		<h1>Interactive School Records Chatbot</h1>
		<p>
			Explore the school records through an AI-powered question-answering system. Ask about
			teachers, events, or any aspect of the records information. To get started click on one of the
			example questions below or enter your own in to the text box.
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
						<button
							class="ask-again outline"
							title="Ask again"
							on:click={() => handleRetryQuestion(chat.question)}><RefreshCwIcon /></button
						>
						<button
							class="delete-chat outline"
							title="Delete this entry"
							on:click={() => deleteChat(parseInt(timestamp))}><Trash2Icon /></button
						>
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
				These questions were generated by the LLM during the data processing stage. These examples
				are random and change on load. (Some questions may be malformed or inaccurate).
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
	<form on:submit|preventDefault={handleSubmit}>
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
		<button class="secondary" disabled>Help</button>
		<button class="secondary" on:click={toggleExampleQuestions}>
			{showExampleQuestions ? 'Hide' : 'Show'} examples
		</button>
		<button class="secondary" on:click={() => (showCustomisePrompt = true)}
			>Customise the bot</button
		>
		<button class="secondary" on:click={clearChatHistory}>Clear the chat</button>
	</section>
</section>

{#if showCustomisePrompt}
	<dialog open>
		<article>
			<header>
				<button aria-label="Close" rel="prev" on:click={() => (showCustomisePrompt = false)}
				></button>
				<p>
					<strong>Customise the bot</strong>
				</p>
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
	}

	.chat-history article footer {
		text-align: right;
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
</style>
