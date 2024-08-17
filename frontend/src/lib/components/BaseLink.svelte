<script lang="ts">
	import { base } from '$app/paths';
	import { page } from '$app/stores';

	export let href;
	export let navItem: boolean = false;

	let ariaCurrent: 'page' | 'false' = 'false';

	// ensure the href starts with a forward slash if it doesn't already
	$: processedHref = href.startsWith('/') ? `${base}${href}` : `${base}/${href}`;
	$: ariaCurrent = navItem && $page.url.pathname.startsWith(`${processedHref}`) ? 'page' : 'false';
</script>

<a href={processedHref} aria-current={ariaCurrent} {...$$restProps} on:click>
	<slot />
</a>

<style>
	[aria-current='page'] {
		text-decoration: underline;
	}
</style>
