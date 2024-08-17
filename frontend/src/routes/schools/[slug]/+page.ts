import { getResults } from '$lib/nodes';
import type { School } from '$lib/types';
import { error } from '@sveltejs/kit';
import type { EntryGenerator, PageLoad } from './$types';

export const load = (async ({ params }) => {
	try {
		const school = await import(`$data/schools/${params.slug}.md`);

		return {
			slug: params.slug,
			content: school.default
		};
	} catch (e) {
		error(404, `Error loading school "${params.slug}": ${(e as Error).message}`);
	}
}) satisfies PageLoad;

export const entries = (async () => {
	const results = await getResults();
	const schools = await results.schools;

	return schools.map((school: School) => ({ slug: school.slug }));
}) satisfies EntryGenerator;
