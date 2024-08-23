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
	let maxCount = 2;
	let sortByLabel = true;

	$: if (data && chartData) {
		filteredData = data
			?.filter((item) => item.count >= minCount)
			.filter((item) => item.count <= maxCount)
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
	$: labelAsTitle = `${label[0].toUpperCase()}${label.slice(1)}`;

	onMount(() => {
		chartData = {
			labels: data.map((item) => item.name),
			datasets: [
				{
					indexAxis: 'y',
					label: `${labelAsTitle} count`,
					data: data.map((item) => item.count)
				}
			]
		};

		filteredSchools = schools;

		maxCount = Math.max(...data.map((item) => item.count));
	});
</script>

<article>
	<h2>Filter the data</h2>
	<form>
		<fieldset class="grid">
			<label
				>Choose a {label}
				<select name="options" id="options" bind:value={selected}>
					<option value=""></option>
					{#each data as item}
						<option value={item.name}>{item.name}</option>
					{/each}
				</select>
			</label>
		</fieldset>
		<fieldset class="grid">
			<label
				>Minimum {label} count: <strong>{minCount}</strong>
				<input type="number" name="minCount" id="minCount" bind:value={minCount} min="1" max="10" />
			</label>
			<label
				>Maximum {label} count: <strong>{maxCount}</strong>
				<input type="number" name="maxCount" id="maxCount" bind:value={maxCount} min="1" max="10" />
			</label>
		</fieldset>
		<fieldset class="grid">
			<p>Sort chart:</p>
			<label
				><input
					name="terms"
					type="radio"
					value={true}
					bind:group={sortByLabel}
				/>Alphabetical</label
			>
			<label>
				<input name="terms" type="radio" value={false} bind:group={sortByLabel} />Count
			</label>
		</fieldset>
	</form>
</article>

<section>
	<article>
		<h2>Results</h2>
		{#if chartData}
			<section>
				<h3>{labelAsTitle} distribution</h3>
				<Bar data={chartData} options={{ responsive: true }} />
			</section>
		{/if}

		<section>
			<h3>Schools</h3>
			{#each filteredSchools as school}
				<h4><BaseLink href="schools/{school.slug}">{school.name}</BaseLink></h4>
				<ul>
					{#each school[field] as value}
						<li>
							{#if value === selected}<mark>{value}</mark>{:else}{value}{/if}
						</li>
					{/each}
				</ul>
			{/each}
		</section>
	</article>
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
