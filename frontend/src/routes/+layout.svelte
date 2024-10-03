<script lang="ts">
	import BaseLink from '$lib/components/BaseLink.svelte';
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import * as config from '$lib/config';
	import { GithubIcon } from 'lucide-svelte';
	import { dev } from '$app/environment';

	import '@picocss/pico/css/pico.css';
	import '@picocss/pico/css/pico.colors.css';

	import '../app.css';

	const version = import.meta.env.APP_VERSION;
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
				<li><BaseLink href="about" navItem={true}>About</BaseLink></li>
				<li><BaseLink href="schools" navItem={true}>School records</BaseLink></li>
				<li><BaseLink href="chat" navItem={true}>Chat</BaseLink></li>
				<li><BaseLink href="keywords" navItem={true}>Keywords</BaseLink></li>
				<li><BaseLink href="topics" navItem={true}>Topics</BaseLink></li>
				<li><BaseLink href="organisations" navItem={true}>Organisations</BaseLink></li>
				<li><BaseLink href="map" navItem={true}>Map</BaseLink></li>
				<li class="separator">|</li>
				<li><ThemeToggle /></li>
			</ul>
		</nav>
	</header>
	<main class="container"><slot /></main>
	<footer class="container">
		<section class="disclaimer">
			This is a prototype designed to stimulate discussion about the use of AI with Indigenous data.
			It may contain errors, inconsistencies, or unexpected behaviors. While exploring, consider the
			potential benefits and challenges of using AI to interact with Indigenous records. How might
			it change our approach to research? What ethical considerations arise? Please use the
			information provided with caution and verify important details. Your feedback and reflections
			on this AI application are valuable for both improving the system and fostering a broader
			dialogue on AI in Indigenous data contexts.
		</section>
		<nav>
			<ul>
				<li><BaseLink href="/">{config.title}</BaseLink></li>
				<li class="separator">|</li>
				<li>Designed and developed by <a href="https://kdl.kcl.ac.uk/">King's Digital Lab</a></li>
			</ul>
			<ul>
				<li>
					<code class="version">
						<a href="https://github.com/kingsdigitallab/iReal/blob/v{version}/CHANGELOG.md">
							v{version}
						</a>
					</code>
				</li>
				<li>
					<a href={config.github} aria-label="GitHub repository">
						<GithubIcon />
					</a>
				</li>
			</ul>
		</nav>
	</footer>
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

	.separator {
		color: var(--pico-muted-border-color);
	}

	main {
		margin-block: var(--pico-block-spacing-vertical);
		height: 100%;
	}

	footer,
	footer nav {
		border-top: 1px solid var(--pico-muted-border-color);
		font-size: 0.8rem;
		margin-block: var(--pico-block-spacing-vertical);
		padding-block: var(--pico-block-spacing-vertical);
	}

	.disclaimer {
		color: var(--pico-muted-color);
		text-align: justify;
	}
</style>
