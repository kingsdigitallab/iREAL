import { getSchoolNodes, getSchools } from '$lib/nodes';
import { error } from '@sveltejs/kit';
import type { EntryGenerator, PageLoad } from './$types';

export const load = (async ({ params, parent }) => {
	try {
		const parentData = await parent();
		const schools = parentData.schools;

		const md = import(`$data/schools/${params.slug}.md`);
		const nodes = getSchoolNodes(params.slug);
		const school = schools.find((s) => s.slug === params.slug);

		return {
			slug: params.slug,
			md,
			nodes,
			school
		};
	} catch (e) {
		error(404, `Error loading school "${params.slug}": ${(e as Error).message}`);
	}
}) satisfies PageLoad;

export const entries = (async () => {
	const schools = await getSchools();

	return schools.map((school) => ({ slug: school.slug }));
}) satisfies EntryGenerator;
