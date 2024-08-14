import { getResults } from '$lib/nodes';
import type { PageServerLoad } from './$types';

export const load = (async () => {
	return {
		results: getResults()
	};
}) satisfies PageServerLoad;
