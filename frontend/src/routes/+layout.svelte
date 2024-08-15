<script lang="ts">
	import ThemeToggle from '$lib/components/ThemeToggle.svelte';
	import * as config from '$lib/config';
	import { GithubIcon } from 'lucide-svelte';

	import '@picocss/pico/css/pico.amber.css';

	const version = import.meta.env.APP_VERSION;
</script>

<svelte:head>
	<title>{config.title}</title>
</svelte:head>

<div class="layout">
	<header class="container">
		<nav>
			<ul>
				<li><a href="/"><strong>{config.title}</strong></a></li>
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
	<footer class="container"></footer>
</div>

<style>
	.layout {
		display: grid;
		grid-template-rows: auto 1fr auto;
		align-items: start;
		min-height: 100vh;
	}

	header {
		border-bottom: 1px solid #ccc;
	}

	main {
		margin-block: var(--pico-block-spacing-vertical);
	}
</style>
