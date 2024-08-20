<script lang="ts">
	import type { Facet } from '$lib/types';
	import {
		BarController,
		BarElement,
		CategoryScale,
		Colors,
		Chart,
		Legend,
		LinearScale,
		Title,
		Tooltip,
		type ChartData
	} from 'chart.js';
	import { onMount } from 'svelte';
	import { Bar } from 'svelte-chartjs';

	Chart.register(
		BarController,
		BarElement,
		CategoryScale,
		Colors,
		Legend,
		LinearScale,
		Title,
		Tooltip
	);
	Chart.defaults.font.family = 'Source Sans Pro';

	export let data: Facet[];
	export let label: string;

	let filteredData;
	let chartData: ChartData;
	let minCount = 2;
	let sortByLabel = true;

	$: if (data && chartData) {
		filteredData = data?.filter((item) => item.count >= minCount);
		if (!sortByLabel) {
			filteredData = filteredData.sort((a, b) => b.count - a.count);
		}

		chartData.labels = filteredData.map((item) => item.name);
		chartData.datasets[0].data = filteredData.map((item) => item.count);
	}

	onMount(() => {
		chartData = {
			labels: data.map((item) => item.name),
			datasets: [
				{
					indexAxis: 'y',
					label: `${label[0].toUpperCase()}${label.slice(1)} count`,
					data: data.map((item) => item.count)
				}
			]
		};
	});
</script>

<form>
	<fieldset>
		<label
			>Minimum {label} count: <strong>{minCount}</strong>
			<input type="range" name="minCount" id="minCount" bind:value={minCount} min="2" max="10" />
		</label>
		<label>
			<input name="terms" type="checkbox" role="switch" bind:checked={sortByLabel} />
			Sort by {label}
		</label>
	</fieldset>
</form>

{#if chartData}
	<Bar data={chartData} options={{ responsive: true }} />
{/if}
