<script lang="ts">
	import * as config from '$lib/config';

	import '@picocss/pico/css/pico.amber.css';
</script>

<svelte:head>
	<title>{config.title}</title>
</svelte:head>

<div class="layout">
	<header class="container">
		<nav>
			<ul>
				<li><strong>{config.title}</strong></li>
			</ul>
			<ul>
				<li>GitHub</li>
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
