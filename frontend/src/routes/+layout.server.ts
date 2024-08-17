import { getResults } from '$lib/nodes';
import type { LayoutServerLoad } from './$types';

export const load = (async () => {
	return {
		results: getResults()
	};
}) satisfies LayoutServerLoad;
