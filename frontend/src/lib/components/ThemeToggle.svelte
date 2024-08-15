<script>
	import { browser } from '$app/environment';
	import { MoonIcon, SunIcon } from 'lucide-svelte';

	let theme = (browser && localStorage.getItem('data-theme')) || 'light';

	if (browser) {
		const preference = window.matchMedia('(prefers-data-theme: dark)');

		if (preference.matches) {
			theme = 'dark';
		}

		setTheme();

		preference.addEventListener('change', (mediaQuery) => {
			if (mediaQuery.matches) {
				theme = 'dark';
			} else {
				theme = 'light';
			}

			setTheme();
		});
	}

	function setTheme() {
		document.documentElement.setAttribute('data-theme', theme);
		localStorage.setItem('data-theme', theme);
	}

	function handleThemeToggle() {
		theme = theme === 'light' ? 'dark' : 'light';

		setTheme();
	}
</script>

<svelte:head>
	<script type="module">
		let theme = localStorage.getItem('data-theme') || 'light';
		const preference = window.matchMedia('(prefers-data-theme: dark)');

		if (preference.matches) {
			theme = 'dark';
		}

		document.documentElement.setAttribute('data-theme', theme);
		localStorage.setItem('data-theme', theme);
	</script>
</svelte:head>

<div class="theme-toggle">
	<a on:click={handleThemeToggle} aria-label="Toggle colour scheme">
		{#if theme === 'light'}
			<MoonIcon />
		{:else}
			<SunIcon />
		{/if}
	</a>
</div>
