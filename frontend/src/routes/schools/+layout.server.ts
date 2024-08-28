import { getSchools } from '$lib/nodes';
import type { LayoutServerLoad } from './$types';

export const load = (async () => {
	return {
		schools: await getSchools()
	};
}) satisfies LayoutServerLoad;
