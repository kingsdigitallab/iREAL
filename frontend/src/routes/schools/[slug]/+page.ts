import { getResults, getSchoolNodes } from '$lib/nodes';
import type { School } from '$lib/types';
import { error } from '@sveltejs/kit';
import type { EntryGenerator, PageLoad } from './$types';

export const load = (async ({ params }) => {
	try {
		const school = import(`$data/schools/${params.slug}.md`);
		const nodes = getSchoolNodes(params.slug);

		return {
			slug: params.slug,
			school,
			nodes
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
