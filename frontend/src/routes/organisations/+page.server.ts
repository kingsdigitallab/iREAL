import { getSchools } from '$lib/nodes';
import type { PageServerLoad } from './$types';

export const load = (async () => {
	const schools = getSchools();

	return {
		schools
	};
}) satisfies PageServerLoad;
