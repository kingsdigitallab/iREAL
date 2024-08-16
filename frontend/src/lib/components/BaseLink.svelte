<script>
	import { base } from '$app/paths';

	export let href;

	// ensure the href starts with a forward slash if it doesn't already
	$: processedHref = href.startsWith('/') ? `${base}${href}` : `${base}/${href}`;
</script>

<a href={processedHref} {...$$restProps} on:click>
	<slot />
</a>

<style>
	.title {
		font-size: var(--font-size-4);
		font-weight: bold;
		margin-block: 0;
	}
</style>
