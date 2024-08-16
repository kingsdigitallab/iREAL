<script lang="ts">
	import BaseLink from '$lib/components/BaseLink.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import * as config from '$lib/config';
	import { GithubIcon } from 'lucide-svelte';
	import { dev } from '$app/environment';

	import '@picocss/pico/css/pico.css';
	import '@picocss/pico/css/pico.colors.css';

	import '../app.css';
</script>

<svelte:head>
	<title>{config.title}</title>
</svelte:head>

<div class="layout">
	<header class="container">
		<nav>
			<ul>
				<li>
					<BaseLink href="/"><strong>{config.title}</strong></BaseLink>
					{#if dev}<mark>dev</mark>{/if}
				</li>
			</ul>
			<ul>
				<li>
					<a href={config.github} aria-label="GitHub repository"><GithubIcon /></a>
				</li>
				<li><ThemeToggle /></li>
			</ul>
		</nav>
	</header>
	<main class="container"><slot /></main>
	<footer class="container"><BaseLink href="/"><small>{config.title}</small></BaseLink></footer>
</div>

<style>
	.layout {
		display: grid;
		grid-template-rows: auto 1fr auto;
		align-items: start;
		min-height: 100vh;
	}

	header {
		border-bottom: 1px solid var(--pico-primary-border);
	}

	main {
		margin-block: var(--pico-block-spacing-vertical);
	}

	footer {
		border-top: 1px solid var(--pico-muted-border-color);
		margin-block: var(--pico-block-spacing-vertical);
		padding-block: var(--pico-block-spacing-vertical);
	}
</style>
