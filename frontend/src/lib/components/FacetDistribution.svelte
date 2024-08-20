<script lang="ts">
	import type { Facet, School } from '$lib/types';
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
	import BaseLink from './BaseLink.svelte';

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
	export let schools: School[];
	export let label: string;
	export let field: string;

	let filteredData: Facet[] = [];
	let filteredSchools: School[] = [];
	let chartData: ChartData;

	let selected: string = '';
	let minCount = 2;
	let sortByLabel = true;

	$: if (data && chartData) {
		filteredData = data
			?.filter((item) => item.count >= minCount)
			.filter((item) => !selected || item.name === selected);
		if (!sortByLabel) {
			filteredData = filteredData.sort((a, b) => b.count - a.count);
		}

		filteredSchools = schools?.filter(
			(school) => !selected || school[field as keyof School].some((value) => value === selected)
		);

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

		filteredSchools = schools;
	});
</script>

<form>
	<fieldset>
		<label
			>Filter by {label}
			<select name="options" id="options" bind:value={selected}>
				<option value=""></option>
				{#each data as item}
					<option value={item.name}>{item.name}</option>
				{/each}
			</select>
		</label>
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

<section>
	<h2>Schools</h2>
	{#each filteredSchools as school}
		<h3><BaseLink href="schools/{school.slug}">{school.name}</BaseLink></h3>
		<ul>
			{#each school[field] as value}
				<li>{value}</li>
			{/each}
		</ul>
	{/each}
</section>

<style>
	ul li {
		display: inline;
		list-style: none;
	}

	li + li::before {
		content: ', ';
	}
</style>
