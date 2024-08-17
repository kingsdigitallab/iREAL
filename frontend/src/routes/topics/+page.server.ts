import type { PageServerLoad } from './$types';

export const load = (async ({ parent }) => {
	const parentData = await parent();
	const results = await parentData.results;

	return {
		results
	};
}) satisfies PageServerLoad;
