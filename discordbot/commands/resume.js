const { SlashCommandBuilder } = require("@discordjs/builders")

module.exports = {
	data: new SlashCommandBuilder().setName("resume").setDescription("Resumes the music"),
	run: async ({ client, interaction }) => {
		const queue = client.player.getQueue(interaction.guildId)

		if (!queue) return await interaction.editReply("You gonna put some songs in the queue or what?")

		queue.setPaused(false)
        await interaction.editReply("Lets restart the party!")
	},
}
