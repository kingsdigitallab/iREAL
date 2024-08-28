import { getSchools } from '$lib/nodes';
import type { PageServerLoad } from './$types';

export const load = (async () => {
	return {
		schools: await getSchools()
	};
}) satisfies PageServerLoad;
