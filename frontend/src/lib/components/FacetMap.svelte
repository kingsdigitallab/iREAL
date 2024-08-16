<script lang="ts">
	import maplibregl from 'maplibre-gl';
	import { onDestroy, onMount } from 'svelte';
	import 'maplibre-gl/dist/maplibre-gl.css';
	import type { Facet } from '$lib/types';

	const { Map, Marker, NavigationControl, Popup } = maplibregl;

	export let places: Facet[];
	export let show = true;

	let map: Map | null = null;

	let mapContainer: HTMLDivElement;

	$: markers = places.map((place) => {
		const coords = place.coords;

		const numberOfSchools = place.schools.length;
		let markerSize = 'single';

		if (numberOfSchools > 5) {
			markerSize = 'lg';
		} else if (numberOfSchools > 3) {
			markerSize = 'md';
		} else if (numberOfSchools > 1) {
			markerSize = 'sm';
		}

		return {
			place: place.name,
			coords: [coords[1], coords[0]],
			markerSize,
			numberOfSchools: numberOfSchools,
			schools: place.schools
		};
	});

	function addMarkerAction(node: HTMLDivElement, { place, coords, schools }) {
		const popupContent = createPopupContent(place, schools);
		const marker = new Marker({ element: node })
			.setLngLat(coords)
			.setPopup(new Popup().setHTML(popupContent))
			.addTo(map);

		return {
			destroy() {
				marker?.remove();
			}
		};
	}

	function createPopupContent(place: string, schools: string[]) {
		let html = `<div class="tooltip">`;
		const items = schools.map((school) => `<li>${school}</li>`).join('');

		return `${html}<h3>${place}</h3><ol>${items}</ol></div>`;
	}

	onMount(() => {
		map = new Map({
			container: mapContainer,
			style: 'https://api.maptiler.com/maps/positron/style.json?key=brTBbnRxuiKp6PgjwFPr',
			center: [146.921099, -31.2532183],
			zoom: 5
		});

		map.addControl(new NavigationControl({ showCompass: true, showZoom: true }));
	});

	onDestroy(() => map?.remove());
</script>

<div class="map" class:hidden={!show} bind:this={mapContainer}>
	{#if map && markers}
		{console.log('markers', markers)}
		{#each markers as marker}
			<div
				use:addMarkerAction={{
					place: marker.place,
					coords: marker.coords,
					schools: marker.schools
				}}
				class="marker"
				class:single={marker.markerSize === 'single'}
				class:sm={marker.markerSize === 'sm'}
				class:md={marker.markerSize === 'md'}
				class:lg={marker.markerSize === 'lg'}
				role="complementary"
			>
				{#if marker.numberOfSchools > 1}
					<span>{marker.numberOfSchools}</span>
				{/if}
			</div>
		{/each}
	{/if}
</div>

<style>
	.map {
		border: 1px solid var(--pico-muted-border-color);
		font-family: var(--pico-font-family);
		height: 600px;
		width: 100%;

		& .maplibregl-popup-content {
			background-color: var(--pico-background-color);
			height: 200px;
			overflow: scroll;
			padding-block: 1rem;
			padding-inline: 1rem;
			scrollbar-color: var(--pico-background-color) transparent;
		}

		& button {
			background: none;
			border: none;
			color: var(--pico-primary-color);
			line-height: unset;
			margin-bottom: unset;
			padding: unset;
		}

		& ol {
			list-style: inside;
			padding-left: 0;
		}
	}

	.marker {
		--marker-size: 12px;

		background-color: var(--pico-color-azure-200);
		border-radius: 50%;
		border: none;
		box-shadow: var(--pico-button-box-shadow);
		color: var(--pico-color);
		cursor: pointer;
		display: block;
		font-size: var(--pico-font-size);
		height: var(--marker-size);
		line-height: var(--marker-size);
		padding: 0;
		text-align: center;
		width: var(--marker-size);
	}

	.marker:hover {
		filter: brightness(90%);
	}

	.sm {
		--marker-size: 24px;

		background-color: var(--pico-color-azure-400);
	}

	.md {
		--marker-size: 36px;

		background-color: var(--pico-color-azure-600);
		color: white;
	}

	.lg {
		--marker-size: 50px;

		background-color: var(--pico-color-azure-800);
		color: white;
	}

	.hidden {
		display: none;
	}
</style>
