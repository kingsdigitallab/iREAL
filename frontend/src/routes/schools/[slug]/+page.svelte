<script lang="ts">
	import type { PageData } from './$types';

	export let data: PageData;

	let { slug, meta, content } = data;
</script>

<article>
	<hgroup>
		<h1>{slug}</h1>
	</hgroup>
	<svelte:component this={content} />
</article>