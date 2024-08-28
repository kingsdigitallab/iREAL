import { getOverview } from '$lib/nodes';
import type { LayoutServerLoad } from './$types';

export const load = (async () => {
	return {
		overview: getOverview()
	};
}) satisfies LayoutServerLoad;
